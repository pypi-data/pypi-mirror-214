import logging
import scipy
import numpy as np
import numpy.typing as npt

from pyfairsim.sim_algorithm.SIM_Parameters import Parameters

logger = logging.getLogger(__name__)

import matplotlib.pyplot as plt


def plot_img(img, title):
    plt.imshow(np.real(img), cmap="gray")
    plt.title(title)
    plt.show()


class Wiener_Filter:
    def __init__(self, parameters: Parameters) -> None:
        self.parameters = parameters
        self._update_cache()

    def _update_cache(self) -> None:
        """
        Setup the Wiener filter. This (re)initiates the cached
        filter values. Has to be called if the OTF or the shift parameters change.
        """
        h, w = (
            2 * self.parameters.image_parameters.image_shape[0],
            2 * self.parameters.image_parameters.image_shape[1],
        )
        self.wiener_denominator = np.zeros((h, w), dtype=np.complex128)
        self.otf_array = np.zeros((h, w), dtype=np.complex128)
        self.otf_array[
            h // 4 : (3 * h) // 4, w // 4 : (3 * w) // 4
        ] += np.fft.ifftshift(self.parameters.get_otf(attenuated=False))
        self.attenuated_otf_array = np.zeros((h, w), dtype=np.complex128)
        self.attenuated_otf_array[
            h // 4 : (3 * h) // 4, w // 4 : (3 * w) // 4
        ] += np.fft.ifftshift(self.parameters.get_otf(attenuated=True))

        # loop directions, bands
        for direction in range(len(self.parameters.directions)):
            for band in range(self.parameters.directions[direction].number_bands):
                self._add_wiener_denominator(
                    direction, band, self.parameters.sim_parameters.use_attenuation
                )

    def _add_wiener_denominator(
        self,
        direction_index: int,
        band_index: int,
        use_attenuation: bool,
        return_array=False,
    ) -> None:
        """
        Add OTF^2, for band and direction, to a vector.
        @param vec input vector
        @param direction_index Direction
        @param band_index Band"""
        direction = self.parameters.directions[direction_index]
        kx = direction.px * band_index
        ky = direction.py * band_index

        otf_array_plus = scipy.ndimage.shift(self.otf_array, (ky, kx))
        otf_array_minus = scipy.ndimage.shift(self.otf_array, (-ky, -kx))
        if use_attenuation:
            otf_array_plus *= scipy.ndimage.shift(self.attenuated_otf_array, (ky, kx))
            otf_array_minus *= scipy.ndimage.shift(
                self.attenuated_otf_array, (-ky, -kx)
            )
        else:
            otf_array_plus = np.abs(otf_array_plus) ** 2
            otf_array_minus = np.abs(otf_array_minus) ** 2

        otf_array_plus = np.fft.ifftshift(otf_array_plus)
        otf_array_minus = np.fft.ifftshift(otf_array_minus)
        if not return_array:
            self.wiener_denominator += otf_array_minus + otf_array_plus
        else:
            return otf_array_minus + otf_array_plus

    def get_denominator(self, wiener_parameter: float) -> npt.ArrayLike:
        """
        Returns reciproc Wiener denominator.
        'Reciproc' means the vector can directly be multiplied to spectrum.
        """
        ret = np.copy(self.wiener_denominator)
        return 1 / (ret + wiener_parameter ** 2)

    def get_widefield_denominator(self, wiener_parameter: float) -> npt.ArrayLike:
        h, w = (
            2 * self.parameters.image_parameters.image_shape[0],
            2 * self.parameters.image_parameters.image_shape[1],
        )
        ret = np.zeros((h, w), dtype=np.complex128)
        ret += self._add_wiener_denominator(
            0, 0, use_attenuation=False, return_array=True
        )
        return 1 / (ret + wiener_parameter ** 2)
