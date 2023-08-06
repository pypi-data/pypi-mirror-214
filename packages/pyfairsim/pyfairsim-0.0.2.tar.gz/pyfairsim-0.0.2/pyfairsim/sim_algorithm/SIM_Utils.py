import logging
from typing import Any, Optional, List, Tuple
import scipy
#import cProfile
import numpy as np
import numpy.typing as npt
from multiprocessing import Pool
from pyfairsim.sim_algorithm.OTF_Provider import (
    get_apotization_array,
    get_attenuation_array,
)
from pyfairsim.sim_algorithm.SIM_Parameters import Parameters
from pyfairsim.sim_algorithm.Wiener_Filter import Wiener_Filter
import matplotlib.pyplot as plt
from pyfairsim.utils.tif import save_tif

logger = logging.getLogger(__name__)


def plot_img(img, title):
    plt.imshow(np.real(img), cmap="gray")
    plt.title(title)
    plt.show()


def plot_fft(fft, title=""):
    plt.imshow(np.log10(np.abs(np.fft.fftshift(fft))), cmap="gray")
    plt.title(title + " in feq. region")
    plt.show()


def plot_ps(fft, peak=None, distance=None, title=""):
    """
    Function to plot the powerspectrum used for a fit and show where the peak was found and what range was excluded
    @param fft input array/image
    @param peak (kx, ky) tuple that contains the peak position if set a circle around the peak will be drawn
    @param distance that was excluded from the search if set the circle will be drawn
    @param title string to add to the title of the plot
    """
    pw = np.copy(fft)
    h, w = pw.shape
    pw = np.log10(np.abs(pw))
    # shift DC component to the center
    pw = np.fft.fftshift(pw)
    pw2 = np.copy(pw)

    if not distance == None:
        for x in range(w):
            for y in range(h):
                # check if the current position is close to the circle and if so color it white
                if (
                    np.hypot(x - w / 2, y - h / 2) < distance
                ):  # + 0.5 and np.hypot(x-w/2, y-h/2) > distance - 0.5:
                    pw2[y][x] = pw[0][0]

    mi = np.min(pw2)
    ma = np.max(pw2)
    if ma - mi > 30:
        mi = ma - 30
    pw = (pw - mi) / (ma - mi)
    ma = ma / (ma - mi)
    pw[pw < 0.8] = 0

    if not distance == None:
        for x in range(w):
            for y in range(h):
                # check if the current position is close to the circle and if so color it white
                if (
                    np.hypot(x - w / 2, y - h / 2) < distance + 0.5
                    and np.hypot(x - w / 2, y - h / 2) > distance - 0.5
                ):
                    pw[y][x] = 1

    if len(peak) == 2:
        kx = w / 2 - peak[0]  # if peak[0] > 0 else peak[0] + w
        ky = h / 2 + peak[1]  # if peak[1] < 0 else h - peak[1]
        title += f" peak at ({kx}, {ky})"
        r = 10  # radius of the circle around the peak
        for x in range(w):
            for y in range(h):
                # check if the current position is close to the peak and if so color it white
                dis = np.hypot(x - kx, y - ky)
                if dis < r + 0.5 and dis > r - 0.5:
                    pw[y][x] = 1

    # save_tif(pw, f"{os.curdir}/power_{title}_feq_region.tif")
    plt.imshow(pw, cmap="gray")
    plt.title(f"power {title} in feq. region")
    plt.show()


def get_fwhm(fwhm_fairsim: float, pixel_size: float) -> float:
    """
    Calculates the fwhm for attenuation generated with @OTF_Provider.get_attenuation_array() from the FairSIM parameters
    fwhm_fairsim: fwhm as used in FairSIM in cycles/micron
    pixel_size: pixel size in micron
    """
    return fwhm_fairsim * pixel_size


def calc_separation_matrix(
    phases: npt.ArrayLike, scalings: List[float], bands: int
) -> npt.ArrayLike:
    """
    Obtain a separation matrix for arbitrary amount of bands.
    Note: Not really tested with more than 3 bands yet.
    If #phases > #bands*2-1, pseudo-inverse will be used.
    @param phases Phases 0..2pi, order: phases[band-1][#phase]
    @param bands  Number bands (2 for 2beam, 3 for 3beam data, ..)
    @param scalings  Scaling factors, one for each band
    @return Inverted band separation matrix
    """
    number_phases = len(phases[0])
    if scalings == None:
        scalings = [1.0 if i == 0 else 0.5 for i in range(bands)]
    else:
        for index in range(1, len(scalings)):
            scalings[index] *= 0.5

    matrix = np.zeros((number_phases, bands * 2 - 1), dtype=complex)
    m, n = matrix.shape
    for phase in range(number_phases):
        # band zero is one, DC component (col 0)
        matrix[phase][0] = scalings[0]
        # all other bands: two phases per band (2 dirac peaks)
        for band in range(bands - 1):
            # pos. dirac peak (cols 1,3,5..)
            matrix[phase][2 * band + 1] = scalings[band + 1] * (
                np.cos(phases[band][phase]) + 1j * np.sin(phases[band][phase])
            )
            # neg. dirac peak (cols 2,4,6..)
            matrix[phase][2 * band + 2] = scalings[band + 1] * (
                np.cos(-phases[band][phase]) + 1j * np.sin(-phases[band][phase])
            )
    if m == n:  # calculate inverse matrix and return
        return np.linalg.inv(matrix)
    else:  # calculate pseudoinverse matrix (A+ = (A* A)^-1 A*) and return
        return (
            np.linalg.inv((matrix.conj().T @ matrix)) @ matrix.conj().T
        )  # @ is matrix multiplication


def separate_bands(
    input: npt.ArrayLike,
    phases: npt.ArrayLike,
    bands: int,
    scalings: Optional[List[float]] = None,
) -> npt.ArrayLike:
    """
    Compute the spectral separation. This creates the matrix
    first (see {@link #calc_separation_matrix}), then multiplies the spectra.
    Supports arbitrary #phases, if (#phases > bands*2-1), pseudo-inverse matrix is used.
    Phase input array should hold all (absolute) phases for 1. band,
    higher band phases are set to multiplies of base.
    @param input     FFT'd input images, array size: #images = #phases/#bands
    @param phases Phases 0..2pi, length >= (bands*2)-1
    @param bands  Number of bands, convention: 2 for 2beam, 3 for 3beam data
    @param scalings    Scaling factors, one for each band
    """
    h, w = input[0].shape
    out = np.zeros((bands * 2 - 1, h, w), dtype=np.complex64)

    # compute phases for higher bands
    pha = np.zeros((bands - 1, len(phases)))
    for band in range(1, bands):
        for phase in range(len(phases)):
            pha[band - 1][phase] = phases[phase] * band
    # create separation matrix
    separation_matrix = calc_separation_matrix(pha, scalings, bands)
    # multiply, output 0 .. bands*2-1
    for phase in range(len(phases)):
        for band in range(bands * 2 - 1):
            out[band] += separation_matrix[band][phase] * input[phase]

    return out


def locate_peak(crosscorrelation: npt.ArrayLike, min_distance: float) -> Tuple[float]:
    """
    Locates position, magnitute and phase of the highest peak in 'crosscorrelation'.
    @param crosscorrelation input vector (typ. cross-/auto-correlation)
    @param min_distance Mininum distance from DC component, in pxl
    @return px, py, mag, phase
    """
    h, w = crosscorrelation.shape

    x_pos, y_pos, maximum, phase = -1, 1, np.min(np.abs(crosscorrelation)), 0.0
    # since if we dont find a max we negate the y we should set it to 1 so this returns -1

    for y in range(h):
        for x in range(w):
            # distance to DC component
            rad = np.sqrt(
                (x ** 2 if x < w / 2 else (x - w) ** 2)
                + (y ** 2 if y < h / 2 else (y - h) ** 2)
            )
            if rad > min_distance and np.abs(crosscorrelation[y][x]) > maximum:
                maximum = np.abs(crosscorrelation[y][x])
                x_pos = x
                y_pos = y
                phase = np.angle(crosscorrelation[y][x])

    # convert to our coordinate convention
    if x_pos > w / 2:
        x_pos = x_pos - w
    if y_pos > h / 2:
        y_pos = h - y_pos
    else:
        y_pos *= -1

    return x_pos, y_pos, maximum, phase


def fit_peak(
    band_0: npt.ArrayLike,
    band_1: npt.ArrayLike,
    band_0_index: int,
    band_1_index: int,
    parameters: Parameters,
    kx: float,
    ky: float,
    weight_limit: float,
    search: float,
) -> Tuple[Any]:
    """
    Fits SIM parameters by cross-correlation of common frequency components.
    Correlates band0 vs. band1, with band1 shifted to kx,ky.

    @param band_0 Low freq band to correlate to (that does not change position)
    @param band_1 High freq band to correlate
    @param band_0_index  Number of the low band (usually 0)
    @param band_1_index  Number of the high band (usually 1 or 2)
    @param cutoff cutoff for the otf
    @param kx Starting guess kx
    @param ky Starting guess ky
    @param weight_Limit If > 0, consider only freq where both weights are over this limit
    @param search kx,ky will be varied +-search
    @return [px, py, mag, phase] and cntrl control vector (size 30x10) to be filled with power spectra, may be null
    """
    # ToDo: check if all arrays are same size

    result_phase = 0
    result_mag = 0
    control = np.zeros((10, 30))

    # loop iterations, each iteration does closer search
    for iteration in range(3):
        # copy input data
        b0 = np.copy(band_0)
        b1 = np.copy(band_1)
        # define common region, with current search guess
        common_region(
            b0,
            b1,
            band_0_index,
            band_1_index,
            parameters,
            kx,
            ky,
            0.15,
            weight_limit,
            True,
        )  # ToDo hardcoded parameters
        # go to real space
        b0 = np.fft.ifft2(b0)
        b1 = np.fft.ifft2(b1)

        # store all correlations
        correlations = np.zeros((10, 10), dtype=complex)
        scale = 1.0 / np.sum(np.abs(b0) ** 2)

        tkx = kx
        tky = ky
        ts = search

        for xi in range(10):
            for yi in range(10):
                # compute position to shift to
                x_pos = tkx + ((xi - 4.5) / 4.5) * ts
                y_pos = tky + ((yi - 4.5) / 4.5) * ts

                # copy and fourier-shift band 1
                b1s = np.copy(b1)
                b1s = fourier_shift(b1s, x_pos, -y_pos)

                # get correlation by multiplication, suming elements, scaling by b0
                correlations[yi][xi] = (
                    np.sum(np.conjugate(b0) * b1s) * scale
                )  # ToDo check if this is correct

        # find the maximum, set as new starting point
        maximum = 0
        minimum = (
            np.max(np.abs(correlations)) + 1
        )  # to ensure it is larger than any that can occur
        new_kx = 0
        new_ky = 0
        for yi in range(10):
            for xi in range(10):
                absolute = np.abs(correlations[yi][xi])
                if absolute > maximum:
                    maximum = absolute
                    new_kx = tkx + ((xi - 4.5) / 4.5) * ts
                    new_ky = tky + ((yi - 4.5) / 4.5) * ts
                    result_phase = np.angle(correlations[yi][xi])
                    result_mag = absolute
                if absolute < minimum:
                    minimum = absolute

        # output to control vector
        for yi in range(10):
            for xi in range(10):
                control[yi][xi + iteration * 10] = (
                    np.abs(correlations[yi][xi]) - minimum
                ) / (maximum - minimum)

        # set new guess
        kx = new_kx
        ky = new_ky
        search /= 5

    return ([kx, ky, result_phase, result_mag], control)


def fourier_shift(array: npt.ArrayLike, kx, ky) -> npt.ArrayLike:
    N, _ = array.shape  # Assumes square array
    x = np.outer(np.ones(N), np.array(range(N)))
    y = np.outer(np.array(range(N)), np.ones(N))
    phase_shift = np.exp(1j * 2 * np.pi * (kx * x + ky * y) / N)
    array *= phase_shift
    return array


def common_region(
    band_0: npt.ArrayLike,
    band_1: npt.ArrayLike,
    band_0_index: int,
    band_1_index: int,
    parameters: Parameters,
    kx: float,
    ky: float,
    distance: float,
    weight_limit: float,
    divide_by_otf: bool,
) -> None:
    """
    Determines a common freq region of band0, band1.
    All frequencies where either OTF is below threshhold 'weightLimit'
    are set to zero in both bands. All others are divided by weight (if switch is set).
    @param band0 The lower band, will not be moved
    @param band1 The higher band, shifted to kx,ky
    @param bn0  Number of the low band (usually 0)
    @param bn1  Number of the high band (usually 1 or 2)
    @param cutoff cutoff for the otf
    @param kx x-coordinate of shift
    @param ky y-coordinate of shift
    @param dist Minimal distance (as fraction of hypot(kx,ky)) to band centers (std use 0.15)
    @param weightLimit Components where either OTF is below this limit are set to 0
    @param divideByOtf If set, all components over weightLimit are divided by OTF weight
    """
    # ToDo: check if all arrays are same size
    shape = band_0.shape
    h, w = shape
    weight_0 = parameters.get_otf(attenuated=False)
    weight_1 = parameters.get_otf(attenuated=False)
    wt_0 = parameters.get_otf(kx=kx, ky=ky, attenuated=False)
    wt_1 = parameters.get_otf(kx=-kx, ky=-ky, attenuated=False)

    # set zero if minimal weight not reached in one or both OTFs
    band_0[np.abs(weight_0) < weight_limit] = 0
    band_0[np.abs(wt_0) < weight_limit] = 0
    if divide_by_otf:
        with np.errstate(
            invalid="ignore", divide="ignore"
        ):  # prevents the runtimeWarning to be printed
            band_0 /= weight_0

    band_1[np.abs(weight_1) < weight_limit] = 0
    band_1[np.abs(wt_1) < weight_limit] = 0
    if divide_by_otf:
        with np.errstate(invalid="ignore", divide="ignore"):
            band_1 /= weight_1

    # set zero around DC component
    maximum = np.sqrt(kx ** 2 + ky ** 2)
    y, x = np.ogrid[0 : shape[0], 0 : shape[1]]
    distances = np.sqrt((x - (w / 2)) ** 2 + (y - (h / 2)) ** 2)
    with np.errstate(invalid="ignore", divide="ignore"):
        relative_distances = np.fft.ifftshift(distances) / maximum
    band_0[relative_distances < distance] = 0
    band_0[relative_distances > (1 - distance)] = 0

    shifted_distances = np.sqrt((x - (w / 2) + kx) ** 2 + (y - (h / 2) - ky) ** 2)
    with np.errstate(invalid="ignore", divide="ignore"):
        relative_shifted_distances = np.fft.ifftshift(shifted_distances) / maximum
    band_1[relative_shifted_distances < distance] = 0
    band_1[relative_shifted_distances > (1 - distance)] = 0

    # fix divide by zeros, we want to only divide when the weight is larger then weight_limit but since we else set it to 0 we might aswell divide all and fix all the divide by zeros
    band_0[np.isnan(band_0)] = 0
    band_1[np.isnan(band_1)] = 0


def get_peak(
    band0: npt.ArrayLike,
    band1: npt.ArrayLike,
    band_0_index: int,
    band_1_index: int,
    parameters: Parameters,
    kx: float,
    ky: float,
    weight_limit: float,
) -> complex:
    """
    Get the cross-correlation of two bands. This fourier-shifts b1 to kx,ky, and
    only takes into account regions where both OTFs are over weightLimit
    (Also, a minimum distance of 0.15*hypot(kx,ky) is ensured to the bands centers).
    Result is scaled by |band0|^2, thus might be used as estimate for modulation.
    @param band0 The lower band, will not be moved
    @param band1 The higher band, shifted to kx,ky
    @param bn0  Number of the low band (usually 0)
    @param bn1  Number of the high band (usually 1 or 2)
    @param cutoff cutoff for the otf
    @param kx x-coordinate of shift
    @param ky y-coordinate of shift
    @param weightLimit Limit for taking into account a certain frequence
    """
    # copy input data
    b0 = np.copy(band0)
    b1 = np.copy(band1)
    # define common freq. region
    common_region(
        b0, b1, band_0_index, band_1_index, parameters, kx, ky, 0.15, weight_limit, True
    )
    # plot_ps(b1, "common")

    # go to real space
    b0 = np.fft.ifft2(b0)
    b1 = np.fft.ifft2(b1)
    # plot_img(b0, "b0")
    # plot_img(b1, "b1")

    # Fourier-shift band1 to correct position
    b1 = fourier_shift(b1, kx, -ky)

    # element wise mult of b0 conjugate with b1
    b1 *= np.conjugate(b0)
    # sum, scale by |band2|^2 and return
    return np.sum(b1) / np.sum(np.abs(b0) ** 2)


def paste_freq(
    array: npt.ArrayLike, out_shape: Tuple[int], x_offset: int, y_offset: int
) -> npt.ArrayLike:
    ret = np.zeros(out_shape, dtype=np.complex128)

    hi, wi = array.shape
    ho, wo = out_shape

    for x in range(wi):
        for y in range(hi):
            xo = x if x < wi / 2 else x + wo // 2
            yo = y if y < hi / 2 else y + ho // 2
            xo = (xo + x_offset + wo) % wo
            yo = (yo + y_offset + ho) % ho
            ret[yo][xo] = array[y][x]

    return ret


def estimate_absolute_phases(parameters: Parameters, input_FFT: npt.ArrayLike):
    for angle in range(len(parameters.directions)):
        direction = parameters.directions[angle]
        phases = []
        for i in range(direction.number_phases):
            ac = np.copy(input_FFT[angle][i])
            # ac *= np.conjugate(parameters.otf_attenuated_array)
            correlation = auto_correlation(ac, direction.px, direction.py)
            phases.append(np.angle(correlation))
        direction.phases = np.array(phases)
        logger.info(f"Found phases for {angle} : {phases}")
        direction.has_individual_phases = True
        direction.set_phase_offset(0)


def estimate_absolute_phases_parallel(parameters: Parameters, input_FFT: npt.ArrayLike):
    arg_list = []
    # plot_img(parameters.otf_attenuated_array, "otf_att")
    # plot_img(parameters.otf_array, "otf")
    # return
    for angel_index in range(len(parameters.directions)):
        current_dir = parameters.directions[angel_index]
        for phase in range(current_dir.number_phases):
            arg_list.append(
                (
                    np.copy(input_FFT[angel_index][phase]),
                    current_dir.px,
                    current_dir.py,
                    parameters.get_otf(attenuated=False),
                )
            )
    with Pool(len(parameters.directions) * parameters.directions[0].number_phases) as p:
        results = p.starmap(estimate_absolute_phase, arg_list)
    for angel_index in range(len(parameters.directions)):
        current_dir = parameters.directions[angel_index]
        current_dir.set_phase_offset(0)
        current_dir.has_individual_phases = True
        current_dir.phases = np.array(
            results[
                parameters.directions[0].number_phases
                * angel_index : parameters.directions[0].number_phases
                * angel_index
                + parameters.directions[0].number_phases
            ]
        )
        logger.info(f"Found phases for {angel_index} : {current_dir.phases}")


def estimate_absolute_phase(fft_image, px, py, otf):
    fft_image *= np.conjugate(otf)
    return np.angle(auto_correlation(fft_image, px, py))


def auto_correlation(input: npt.ArrayLike, kx: float, ky: float) -> np.complex128:
    # double the vector size to allow a good shift
    aV = paste_freq(input, (input.shape[0] * 2, input.shape[1] * 2), 0, 0)
    bV = paste_freq(input, (input.shape[0] * 2, input.shape[1] * 2), 0, 0)
    # ToDo need to check if the shift + otf support still fit in the array if so we can use the original else we need to magnify it
    # aV = np.copy(input)
    # bV = np.copy(input)
    # plot_fft(aV, "av")
    # plot_fft(bV, "bv")
    # move one copy to its new position kx, ky
    bV = np.fft.fft2(fourier_shift(np.fft.ifft2(bV), kx, ky))

    # compute the auto-correlation
    product = aV * np.conjugate(bV)
    ret = np.sum(product)

    # normalize (?)
    ret = ret / np.sum(aV * aV)
    return ret


def estimate_parameters_one_direction(
    angel_index: int,
    parameters: Parameters,
    input_FFT: npt.ArrayLike,
    otf_attenuation: npt.ArrayLike,
    keep_phases: bool,
):
    #profiler = cProfile.Profile()
    #profiler.enable()
    current_dir = parameters.directions[angel_index]
    h, w = input_FFT[0][0].shape
    fit_band = parameters.sim_parameters.fit_band

    # idx of low band (phase detection) and high band (shift vector detection)
    # will be the same for two-beam
    low_band = 1
    high_band = 3 if current_dir.number_bands == 3 else 1
    fb = low_band if fit_band == 1 else high_band

    # compute band seperation
    input_copy = np.zeros((current_dir.number_phases, h, w), dtype=complex)
    separate = np.zeros((current_dir.get_number_of_components(), h, w))

    for phase in range(current_dir.number_phases):
        input_copy[phase] = np.copy(input_FFT[angel_index][phase])
        input_copy[phase] *= current_dir.get_intensity_quotient(phase)

    if not keep_phases:
        # reset any previously set phases
        current_dir.reset_phases()
    else:
        raise NotImplementedError("keep_phases not implemented jet")  # ToDo

    phases = current_dir.get_phases()
    phases = np.array(phases)

    separate = separate_bands(input_copy, phases, current_dir.number_bands)
    # ToDo is the line pattern in the difference between this and fairSIM, see file on desktop, relevant?
    # save_tif(separate[0].real, f"separate{angel_index}0.tif")
    # save_tif(separate[1].real, f"separate{angel_index}1.tif")
    # save_tif(separate[2].real, f"separate{angel_index}2.tif")

    # compute correlation: dampen region around DC, ifft, mult. in spatial, fft back
    # save_tif(otf_attenuation, "otfattenuated.tif")
    c_0 = np.fft.ifft2(np.copy(separate[0]) * otf_attenuation)
    c_1 = np.fft.ifft2(np.copy(separate[low_band]) * otf_attenuation)
    c_2 = np.fft.ifft2(np.copy(separate[high_band]) * otf_attenuation)

    c_1 *= np.conjugate(c_0)
    c_2 *= np.conjugate(c_0)

    c_1 = np.fft.fft2(c_1)
    c_2 = np.fft.fft2(c_2)
    # save_tif(c_1.real, "c_1.tif")
    # ToDo same pattern still in difference at 0.03% of the max amplitude of original

    min_distance = 2

    if parameters.sim_parameters.fit_exclude > 0:
        # find the highest peak in corr of band0 to highest band
        # minDist of otfCutoff from origin, store in 'param'
        min_distance = (
            parameters.sim_parameters.fit_exclude
            * parameters.cutoff
            * parameters.image_parameters.image_shape[0]
        )
        peak = locate_peak(c_1 if fit_band == 1 else c_2, min_distance)
    else:
        raise NotImplementedError("fit_exclude not implemented jet")  # ToDo

    # fit the peak to sub-pixel precision by cross-correlation of the Fourier-shifted components
    peak, control = fit_peak(
        separate[0],
        separate[fb],
        0,
        fb,
        parameters,
        -peak[0],
        -peak[1],
        0.05,
        2.5,
    )
    # plot_ps(c_1 if fit_band == 1 else c_2, peak=peak[:2], distance=min_distance)
    # plot_img(control, "control")

    # now, either three beam / 3 bands ...
    if low_band != high_band:
        # peak should contain the shift band0 <-> band2, so if band0 <-> band1 was fitted, multiply by 2
        if fit_band == 1:
            peak[0] *= 2
            peak[1] *= 2

        # at the peak position found, extract phase and modulation from band0 <-> band1
        peak_1 = get_peak(
            separate[0],
            separate[low_band],
            0,
            1,
            parameters,
            peak[0] / 2,
            peak[1] / 2,
            0.05,
        )

        # TODO: this is a quick fix, this should be done properly by looking at the OTF
        # overlap, to figure out if parameter extraction is possible. This just catches
        # the 'definitely not possible' case
        if np.hypot(peak[0], peak[1]) > (
            parameters.cutoff * parameters.image_parameters.image_shape[0]
        ):
            peak_2 = peak_1
        else:
            # extract modulation from band0 <-> band2
            peak_2 = get_peak(
                separate[0],
                separate[high_band],
                0,
                2,
                parameters,
                peak[0],
                peak[1],
                0.05,
            )

        # return the result
        #       px        py       phase_offset      modulation[1]   modulation[2]
        return (-peak[0], peak[1], np.angle(peak_1), np.abs(peak_1), np.abs(peak_2))
    # ... or two-beam / 2 bands
    if low_band == high_band:
        # get everything from one correlation band0 <-> band1
        peak_1 = get_peak(
            separate[0], separate[1], 0, 1, parameters, peak[0], peak[1], 0.05
        )

        #profiler.disable()
        #if angel_index == 0:
        #    profiler.print_stats(sort="tottime")

        # return the result
        #       px        py       phase_offset      modulation[1]   modulation[2]
        return (-peak[0], peak[1], np.angle(peak_1), np.abs(peak_1), -1)


def estimate_parameters(
    parameters: Parameters,
    input_FFT: npt.ArrayLike,
    keep_phases: bool,
) -> None:
    """
    Run the SIM parameter estimation
    @param parameters  The SIM parameter instance to work on
    @param input_FFT  The input images (in Fourier space)
    @param keepPhases If true, phase information from SimParam will be used in band separation
    """
    # input_FFT consists of 4D array 1st and 2nd dimension are band and phase, last two define image dimensions
    fit_band = parameters.sim_parameters.fit_band
    if fit_band != 1 and fit_band != 2:
        raise ValueError("Fitband neither 1 nor 2!")

    shape = input_FFT[0][0].shape

    # The attenuation vector helps well to fade out the DC component,
    # which is uninteresting for the correlation anyway
    attenuation = get_attenuation_array(
        shape, 0.99, 0.15 * parameters.cutoff
    )  # ToDo Hardcoded
    # plot_img(otf_attenuation, "att")
    # plot_img(parameters.get_otf(attenuated=False), "otf")
    # save_tif(np.fft.fftshift(parameters.get_otf(attenuated=False)), "otf.tif")
    arg_list = []
    for angel_index in range(len(parameters.directions)):
        arg_list.append((angel_index, parameters, input_FFT, attenuation, keep_phases))
    with Pool(3) as p:
        results = p.starmap(estimate_parameters_one_direction, arg_list)
    for angel_index, result in enumerate(results):
        px, py, phase_offset, modulation_1, modulation_2 = result
        current_dir = parameters.directions[angel_index]
        current_dir.set_px_py(px, py)
        current_dir.set_phase_offset(phase_offset)
        current_dir.modulations[1] = modulation_1
        if modulation_2 != -1:
            current_dir.modulations[2] = modulation_2
        if py == 0:
            py = 1e-14
        logger.info(
            f"Found {angel_index} peak with shift: ({px:.3f},{py:.3f}), r: {np.hypot(px, py):.3f}, angle: {np.arctan(px/py):.3f} and phase offset {phase_offset:.5f} and modulation {modulation_1:.5f}, {modulation_2:.3f}."
        )


def run_reconstruction(
    parameters: Parameters, inFFT: npt.ArrayLike
) -> List[npt.ArrayLike]:
    """
    Run the SIM reconstruction
    @param parameters  The SIM parameter instance to work on
    @param inFFT  The input images (in Fourier space)
    @param otf_before_shift Apply the OTF before shifting bands
    @param image_clip_scale Clip zero values and scale (0..255) output images?
    @return widefield_result The widefield image computed during the reconstruction (may be null)
    @return filtered_widefield_result The filtered widefield image (may be null)
    @return The reconstructed image */
    """
    h, w = inFFT[0][0].shape
    apo_bend = parameters.filter_parameters.apodization_bend
    apo_cutoff = parameters.filter_parameters.apodization_cutoff
    # setup Wienerfilter
    w_filter = Wiener_Filter(parameters)
    # vector to store the result
    size = parameters.image_parameters.image_shape[0] * 2
    full_result = np.zeros((size, size), dtype=complex)
    low_frequency_result = np.zeros((size, size), dtype=complex)
    # ToDo here RL stuff
    # loop all pattern directions
    for angle_index in range(len(parameters.directions)):
        current_dir = parameters.directions[angle_index]
        separate = [np.zeros((h, w)) for _ in range(current_dir.number_bands * 2 - 1)]
        # copy into temp. array (to not override input data) and apply correction factor
        tmp_array = [np.zeros((h, w)) for _ in range(current_dir.number_phases)]
        for phase in range(current_dir.number_phases):
            tmp_array[phase] = np.copy(inFFT[angle_index][phase])
            tmp_array[phase] *= current_dir.get_intensity_quotient(phase)

        # ToDo here RL stuff
        # use the temp array as input for the band separation
        separate = separate_bands(
            tmp_array,
            current_dir.get_phases(),
            current_dir.number_bands,
            current_dir.get_modulations(),
        )
        # add band 0 to low_frequency_result
        low_frequency_result += paste_freq(separate[0], (2 * h, 2 * w), 0, 0)

        for i in range(current_dir.number_bands * 2 - 1):
            # plot_fft(shifted[i], f"shifted[{i}]")
            # plot_img(np.fft.ifft2(separate[i]), i)
            pass
        # Wiener filter: Apply OTF here
        if (
            parameters.sim_parameters.otf_before_shift and True
        ):  # ToDo True should be replaced by parameter.use_wiener_filter() for now hardcoded wiener filter use
            otf_array = parameters.get_otf()
            for i in range(current_dir.number_bands * 2 - 1):
                # plot_fft(separate[i], f"i separate[{i}], angle: {angle_index}")
                separate[i] *= np.conj(otf_array)
                # plot_fft(separate[i], f"f separate[{i}], angle: {angle_index}")
        # Shifts to correct position
        shifted = [
            np.zeros((2 * h, 2 * w)) for _ in range(5)
        ]  # ToDo why 5 why hardcoded
        # band0 is DC, so does not need shifting, only a bigger vector
        shifted[0] = paste_freq(separate[0], (2 * h, 2 * w), 0, 0)
        # higher bands need shifting
        for band in range(1, current_dir.number_bands):
            positive = band * 2
            negative = band * 2 - 1
            # first copy to larger vectors
            shifted[positive] = paste_freq(separate[positive], (2 * h, 2 * w), 0, 0)
            shifted[negative] = paste_freq(separate[negative], (2 * h, 2 * w), 0, 0)
            # then fourier shift
            shifted[positive] = np.fft.fft2(
                fourier_shift(
                    np.fft.ifft2(shifted[positive]),
                    current_dir.px * band,
                    current_dir.py * band,
                )
            )
            shifted[negative] = np.fft.fft2(
                fourier_shift(
                    np.fft.ifft2(shifted[negative]),
                    -current_dir.px * band,
                    -current_dir.py * band,
                )
            )
        if (
            True
        ):  # ToDo True should be replaced by parameter.use_wiener_filter() for now hardcoded wiener filter use

            if not parameters.sim_parameters.otf_before_shift:
                # multiply with shifted OTF
                otf_array = np.zeros((2 * h, 2 * w), dtype=np.complex128)
                otf_array[
                    2 * h // 4 : (3 * 2 * h) // 4, 2 * w // 4 : (3 * 2 * w) // 4
                ] += np.fft.ifftshift(parameters.get_otf())

                shifted[0] *= otf_array
                for band in range(1, current_dir.number_bands):

                    otf_array_plus = scipy.ndimage.shift(
                        otf_array, (-current_dir.py * band, current_dir.px * band)
                    )
                    otf_array_plus = np.fft.ifftshift(otf_array_plus)
                    otf_array_minus = scipy.ndimage.shift(
                        otf_array, (current_dir.py * band, -current_dir.px * band)
                    )
                    otf_array_minus = np.fft.ifftshift(otf_array_minus)
                    positive = band * 2
                    negative = band * 2 - 1
                    shifted[positive] *= otf_array_plus
                    shifted[negative] *= otf_array_minus
            else:
                otf_array = np.zeros((2 * h, 2 * w), dtype=np.complex128)
                otf_array[
                    2 * h // 4 : (3 * 2 * h) // 4, 2 * w // 4 : (3 * 2 * w) // 4
                ] += np.fft.ifftshift(parameters.get_otf(attenuated=False))
                # or mask for OTF support
                for band in range(1, current_dir.number_bands):
                    positive = band * 2
                    negative = band * 2 - 1
                    otf_array_plus = scipy.ndimage.shift(
                        otf_array, (current_dir.py * band, current_dir.px * band)
                    )
                    otf_array_plus = np.fft.ifftshift(otf_array_plus)
                    otf_array_minus = scipy.ndimage.shift(
                        otf_array, (-current_dir.py * band, -current_dir.px * band)
                    )
                    otf_array_minus = np.fft.ifftshift(otf_array_minus)
                    shifted[positive][otf_array_plus < 1e-7] = 0
                    shifted[negative][otf_array_minus < 1e-7] = 0

        # sum up result
        # ToDo RL
        for i in range(current_dir.number_bands * 2 - 1):
            full_result += shifted[i]
            # plot_fft(shifted[i], f"shifted[{i}]")
            # plot_img(np.fft.ifft2(shifted[i]), i)

        for i in range(current_dir.number_bands):
            band_image = shifted[i * 2]
            if i != 0:
                band_image += shifted[i * 2 - 1]
            # plot_fft(band_image, f"a{angle_index}: band:{i}")
            # plot_img(np.fft.ifft2(band_image), f"a{angle_index}: band:{i}")
            # save_tif(
            #    np.fft.ifft2(band_image).astype(np.float32),
            #    f"shifted{angle_index}{i}.tif",
            # )
    # -- done loop all pattern directions, 'fullResult' now holds the image --

    # Wiener filter on output

    if (
        True
    ):  # ToDo True should be replaced by parameter.use_wiener_filter() for now hardcoded wiener filter use
        # multiply by wiener denominator
        w_den = w_filter.get_denominator(
            parameters.filter_parameters.wiener_filter_parameter
        )
        widefield_wiener_denominator = w_filter.get_widefield_denominator(
            parameters.filter_parameters.wiener_filter_parameter
        )
        # wiener = 1/w_den
        # wiener -= np.min(wiener)
        # wiener /= np.max(wiener)
        # wiener = np.fft.fftshift(wiener)
        # plot_img(wiener, f"w")
        # save_tif(wiener.astype(np.float32), "py_wiener.tif")
        full_result *= w_den

        otf_array = np.zeros_like(low_frequency_result)
        otf_array[
            2 * h // 4 : (3 * 2 * h) // 4, 2 * w // 4 : (3 * 2 * w) // 4
        ] += np.fft.ifftshift(parameters.get_otf(attenuated=False))
        otf_array = np.fft.ifftshift(otf_array)
        low_frequency_result[otf_array < 0.001] = 0
        low_frequency_result *= otf_array
        low_frequency_result *= widefield_wiener_denominator
        # plot_img(w_den, "wfd")
        # save_tif(widefield_wiener_denominator.real, "wfd.tif")

        # apply apotization filter
        # apo = np.zeros((2 * h, 2 * w), dtype=complex)
        # otf.write_apo_vector(apo, apo_bend, apo_cutoff)
        apo = get_apotization_array(
            (2 * h, 2 * w), 1 / 2 * apo_cutoff * parameters.cutoff, apo_bend
        )
        # apo_real = np.fft.fftshift(apo)
        # plot_img(apo_real, f"w")
        # save_tif(apo_real, "apo.tif")
        full_result *= apo
        # plot_fft(full_result, f"full result")

        full_result_image = np.real(
            np.fft.ifft2(full_result)
        )  # ToDo this would need cliping and scaling
        filtered_widefield_image = np.real(np.fft.ifft2(low_frequency_result))

    # ToDo RL

    # print(np.min(full_result_image))
    return [full_result_image, filtered_widefield_image]  # ToDo add widefield
