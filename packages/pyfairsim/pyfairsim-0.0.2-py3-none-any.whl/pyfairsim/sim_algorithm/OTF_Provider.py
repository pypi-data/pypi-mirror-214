import logging
import scipy
import numpy as np
import numpy.typing as npt
from typing import Optional, Tuple, List
import pyfairsim.utils.tif

import matplotlib.pyplot as plt

APPROX_TYPE = ("EXPONENTIAL", "SPHERICAL", "NONE", "FILE")

logger = logging.getLogger(__name__)


def get_attenuation_array(
    size: Tuple[int],
    strength: float,
    fwhm: float,
    k_x: Optional[float] = 0,
    k_y: Optional[float] = 0,
) -> npt.ArrayLike:
    """
    Calculates 2D attenuation array that can be multiplied element wise to an otf to receive an attenuated otf
    size: Tuple of the dimensions for the output array
    strength: strength factor of the gauss
    fwhm: full width at half maximum of the gauss (the FairSIM fwhm needs to be multiplied by the pixel_size)
    k_x/y: shift of center in x/y direction
    """
    # create array containing relative distances to the center size[0]/2, size[1]/2
    y, x = np.ogrid[0 : size[0], 0 : size[1]]
    # delta x = x - k_x - size_x/2 => delta x _relative = delta x / size_x
    relative_distances = np.sqrt(
        ((x - (size[1] / 2 + k_x)) / size[1]) ** 2
        + ((y - (size[0] / 2 - k_y)) / size[0]) ** 2
    )
    # calculate the attenuation
    attenuation = 1 - strength * np.exp(
        -(np.power(relative_distances, 2)) / (2 * np.power(fwhm / 2.355, 2))
    )
    return np.fft.ifftshift(attenuation)


def get_apotization_array(
    size: Tuple[int], cutoff: float, bend: float
) -> npt.ArrayLike:
    """
    Calculates the 2D apotization array
    cutoff: cutoff of the otf used
    bend: bend exponent
    """
    return np.power(get_ideal_otf_array(size, cutoff), bend)


def get_ideal_otf_array(
    size: Tuple[int],
    cutoff: float,
    k_x: Optional[float] = 0,
    k_y: Optional[float] = 0,
    compensation_type: Optional[str] = "",
    a: Optional[float] = 0.15,
) -> npt.ArrayLike:
    """
    Calculates the 2D otf for an ideal lens system, resolution limited by a circular pupil in fourier place.
    "Joseph W. Goodman, Introduction to Fourier Optics, 3. edition, page 145"
    size: Tuple of the dimensions for the output array
    cutoff: normalized cutoff frequency, cutoff = wavelength / (size[0] * pixel_size * NA)
    k_x/y: shift of otf in x/y direction
    compensation_type: Type to compensate for deviations from the ideal otf, can either be EXPONENTIAL or SPHERICAL anything else is treated as None
    a: parameter a for the compensation
    """

    # create array containing relative distances to the center size[0]/2, size[1]/2 and set all distances > 1 to nan
    y, x = np.ogrid[0 : size[0], 0 : size[1]]
    relative_distances = np.sqrt(
        ((x - (size[1] / 2 + k_x)) / size[1]) ** 2
        + ((y - (size[0] / 2 - k_y)) / size[0]) ** 2
    )
    relative_distances[relative_distances > cutoff] = np.nan
    # re-normalize the distances
    relative_distances /= cutoff
    # calculate a ideal otf from relative distances
    otf = (
        2
        / np.pi
        * (
            np.arccos(relative_distances)
            - relative_distances * np.sqrt(1 - relative_distances ** 2)
        )
    )
    # compensate for deviations
    if compensation_type == APPROX_TYPE[0]:  # EXPONENTIAL
        otf *= np.power(a, relative_distances)
    elif compensation_type == APPROX_TYPE[1]:  # SPHERICAL
        otf *= 1 - ((1 - a) * (1 - 4 * np.power(relative_distances - 0.5, 2)))
    # set out of scope otf to 0
    otf[np.isnan(otf)] = 0
    return np.fft.ifftshift(otf)


def shift_otf(otf_array: npt.ArrayLike, kx: float, ky: float) -> npt.ArrayLike:
    if (kx == 0) and (ky == 0):
        # we dont need to shift so no need to calculate
        return np.copy(otf_array)
    return np.fft.ifftshift(scipy.ndimage.shift(np.fft.fftshift(otf_array), (-ky, kx)))


def plot_img(img, title):
    plt.imshow(np.real(img), cmap="gray")
    plt.title(title)
    plt.show()


def get_otf_from_file(filename: str, size: Tuple[int]) -> npt.ArrayLike:
    otf, metadata = pyfairsim.utils.tif.load_tif(filename)
    otf = np.array(otf[0], dtype=np.complex128)
    # scale the image range from 0 to 1
    minimum, maximum = np.min(otf), np.max(otf)
    otf -= minimum
    otf /= maximum - minimum
    if otf.shape != tuple(size):
        raise ValueError(
            f"Shape of otf file ({otf.shape}) and images ({size}) dont match"
        )
    else:
        return np.fft.fftshift(otf)
