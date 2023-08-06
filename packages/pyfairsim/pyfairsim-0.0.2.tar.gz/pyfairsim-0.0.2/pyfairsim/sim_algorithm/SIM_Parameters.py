import logging
from typing import Optional, List, Tuple
from numpy.typing import ArrayLike

from pyfairsim.sim_algorithm.OTF_Provider import (
    get_ideal_otf_array,
    get_attenuation_array,
    get_otf_from_file,
    shift_otf,
)
from pyfairsim.sim_algorithm.Direction import Direction
from pyfairsim.utils.physics import to_SI

logger = logging.getLogger(__name__)


class SIM_Parameters:
    def __init__(
        self,
        otf_correction: float,
        otf_type: str,
        otf_before_shift: bool,
        attenuation_strength: float,
        attenuation_fwhm: float,
        use_attenuation: bool,
        fit_band: int,
        fit_exclude: float,
        otf_file_location=None,
    ):
        self.otf_correction = otf_correction
        self.otf_type = otf_type
        self.otf_before_shift = otf_before_shift
        self.attenuation_strength = attenuation_strength
        self.attenuation_fwhm = attenuation_fwhm
        self.use_attenuation = use_attenuation
        self.fit_band = fit_band
        self.fit_exclude = fit_exclude
        self.otf_file_location = otf_file_location

    def as_dict(self) -> dict:
        out_dict = {}
        out_dict["otf_correction"] = self.otf_correction
        out_dict["otf_type"] = self.otf_type
        out_dict["otf_before_shift"] = self.otf_before_shift
        out_dict["attenuation_strength"] = self.attenuation_strength
        out_dict["attenuation_fwhm"] = self.attenuation_fwhm
        out_dict["use_attenuation"] = self.use_attenuation
        out_dict["fit_band"] = self.fit_band
        out_dict["fit_exclude"] = self.fit_exclude
        out_dict["otf_file_location"] = self.otf_file_location

        return out_dict

    @classmethod
    def from_dict(cls, data_dict: dict) -> "SIM_Parameters":
        otf_correction = data_dict["otf_correction"]
        otf_type = data_dict["otf_type"]
        otf_before_shift = data_dict["otf_before_shift"]
        attenuation_strength = data_dict["attenuation_strength"]
        attenuation_fwhm = data_dict["attenuation_fwhm"]
        use_attenuation = data_dict["use_attenuation"]
        fit_band = data_dict["fit_band"]
        fit_exclude = data_dict["fit_exclude"]
        otf_file_location = data_dict["otf_file_location"]
        return SIM_Parameters(
            otf_correction,
            otf_type,
            otf_before_shift,
            attenuation_strength,
            attenuation_fwhm,
            use_attenuation,
            fit_band,
            fit_exclude,
            otf_file_location,
        )

    @classmethod
    def as_descriptive_dict(cls) -> dict:
        out_dict = {}
        out_dict[
            "otf_correction"
        ] = "Correction factor to account for worse than ideal otfs."
        out_dict[
            "otf_type"
        ] = "Otf type. Currently supported: EXPONENTIAL, SPHERICAL, NONE, FILE"
        out_dict[
            "otf_before_shift"
        ] = "Determines if otf is applied before shifting in the reconstruction"
        out_dict["attenuation_strength"] = "Attenuation strength from 0 .. 1"
        out_dict["attenuation_fwhm"] = "Attenuation full width at half maximum in 1/um"
        out_dict["use_attenuation"] = "if true use attenuation in wiener filter"
        out_dict["fit_band"] = "Which band to do the fit in the parameter estimation"
        out_dict[
            "fit_exclude"
        ] = "If set to false fitting is skipped and the values for kx, ky from this file are used"
        out_dict[
            "otf_file_location"
        ] = "If a otf file is used include the path here, else set it to null"

        return out_dict


class Microscope_Parameters:
    def __init__(self, pixel_size, na, wavelength):
        self.pixel_size = pixel_size
        self.na = na
        self.wavelength = wavelength

    def as_dict(self) -> dict:
        out_dict = {}
        out_dict["pixel_size"] = self.pixel_size
        out_dict["na"] = self.na
        out_dict["wavelength"] = self.wavelength

        return out_dict

    @classmethod
    def from_dict(cls, data_dict) -> "Microscope_Parameters":
        pixel_size = data_dict["pixel_size"]
        na = data_dict["na"]
        wavelength = data_dict["wavelength"]

        return Microscope_Parameters(pixel_size, na, wavelength)

    @classmethod
    def as_descriptive_dict(cls) -> dict:
        out_dict = {}
        out_dict["pixel_size"] = "Resulting pixel size of the microscope in nm"
        out_dict["na"] = "NA of the objective"
        out_dict["wavelength"] = "Emission wavelength of the microscope in nm"

        return out_dict


class Filter_Parameters:
    def __init__(self, wiener_filter_parameter, apodization_cutoff, apodization_bend):
        # filter parameters:
        self.wiener_filter_parameter = wiener_filter_parameter
        self.apodization_cutoff = apodization_cutoff  # in units the abbe limit frequency of the microscope? -> 2 means 2 times resolution of widefield
        self.apodization_bend = apodization_bend

    def as_dict(self) -> dict:
        out_dict = {}
        out_dict["wiener_filter_parameter"] = self.wiener_filter_parameter
        out_dict["apodization_cutoff"] = self.apodization_cutoff
        out_dict["apodization_bend"] = self.apodization_bend

        return out_dict

    @classmethod
    def as_descriptive_dict(cls) -> dict:
        out_dict = {}
        out_dict[
            "wiener_filter_parameter"
        ] = "Wiener filter parameter usual value is 0.05"
        out_dict[
            "apodization_cutoff"
        ] = "Apodization cutoff in units the abbe limit frequency of the microscope. Usual value is 2"
        out_dict[
            "apodization_bend"
        ] = "Apodization bend. Exponent of the exponentiation of the otf. Usual value is 0.9"

        return out_dict

    @classmethod
    def from_dict(cls, data_dict: dict) -> "Filter_Parameters":
        wiener_filter_parameter = data_dict["wiener_filter_parameter"]
        apodization_cutoff = data_dict["apodization_cutoff"]
        apodization_bend = data_dict["apodization_bend"]
        return Filter_Parameters(
            wiener_filter_parameter, apodization_cutoff, apodization_bend
        )


class Image_Parameters:
    def __init__(
        self,
        image_shape: Tuple[int, int],
        ordering: str,
        z_slice: int,
        background: float,
    ):
        self.image_shape = image_shape
        self.ordering = ordering
        self.z_slice = z_slice
        self.background = background

    def as_dict(self) -> dict:
        out_dict = {}
        out_dict["image_shape"] = self.image_shape
        out_dict["ordering"] = self.ordering
        out_dict["z_slice"] = self.z_slice
        out_dict["background"] = self.background

        return out_dict

    @classmethod
    def as_descriptive_dict(cls) -> dict:
        out_dict = {}
        out_dict[
            "image_shape"
        ] = "the image shape as list in pixel. For now only square images."
        out_dict[
            "ordering"
        ] = "the ordering of the images: p for phase, z for z, a for angel."
        out_dict[
            "z_slice"
        ] = "which z slice should be reconstructed. Starts to count from 0"
        out_dict[
            "background"
        ] = "Background value that should be subtracted from the raw data before further processing"

        return out_dict

    @classmethod
    def from_dict(cls, data_dict: dict) -> "Image_Parameters":
        image_shape = data_dict["image_shape"]
        ordering = data_dict["ordering"]
        z_slice = data_dict["z_slice"]
        background = data_dict["background"]
        return Image_Parameters(image_shape, ordering, z_slice, background)


class Parameters:
    def __init__(
        self,
        directions: List[Direction],
        microscope_parameters: Microscope_Parameters,
        sim_parameters: SIM_Parameters,
        filter_parameters: Filter_Parameters,
        image_parameters: Image_Parameters,
    ):
        self.directions = directions
        self.microscope_parameters = microscope_parameters
        self.sim_parameters = sim_parameters
        self.filter_parameters = filter_parameters
        self.image_parameters = image_parameters
        self.cycles = 1 / (
            image_parameters.image_shape[0] * microscope_parameters.pixel_size
        )
        self.cutoff = (
            2
            * self.microscope_parameters.na
            * self.microscope_parameters.pixel_size
            / self.microscope_parameters.wavelength
        )
        self.otf_array = None
        self.otf_attenuated_array = None

    def as_dict(self) -> dict:
        out_dict = {}

        out_dict["directions"] = [d.as_dict() for d in self.directions]
        out_dict["microscope_parameters"] = self.microscope_parameters.as_dict()
        out_dict["sim_parameters"] = self.sim_parameters.as_dict()
        out_dict["filter_parameters"] = self.filter_parameters.as_dict()
        out_dict["image_parameters"] = self.image_parameters.as_dict()

        return out_dict

    @classmethod
    def as_descriptive_dict(cls) -> dict:
        out_dict = {}

        out_dict["directions"] = [Direction.as_descriptive_dict() for _ in range(3)]
        out_dict["microscope_parameters"] = Microscope_Parameters.as_descriptive_dict()
        out_dict["sim_parameters"] = SIM_Parameters.as_descriptive_dict()
        out_dict["filter_parameters"] = Filter_Parameters.as_descriptive_dict()
        out_dict["image_parameters"] = Image_Parameters.as_descriptive_dict()

        return out_dict

    @classmethod
    def from_dict(cls, data_dict) -> "Parameters":
        directions = [Direction.from_dict(d) for d in data_dict["directions"]]
        microscope_parameters = Microscope_Parameters.from_dict(
            data_dict["microscope_parameters"]
        )
        sim_parameters = SIM_Parameters.from_dict(data_dict["sim_parameters"])
        filter_parameters = Filter_Parameters.from_dict(data_dict["filter_parameters"])
        image_parameters = Image_Parameters.from_dict(data_dict["image_parameters"])

        return Parameters(
            directions,
            microscope_parameters,
            sim_parameters,
            filter_parameters,
            image_parameters,
        )

    def get_otf(self, kx=None, ky=None, attenuated=None) -> ArrayLike:
        if type(self.otf_array) == type(None):
            self._load_otf()
        if kx == None:
            kx = 0
        if ky == None:
            ky = 0
        if attenuated == None:
            otf = (
                self.otf_attenuated_array
                if self.sim_parameters.use_attenuation
                else self.otf_array
            )
        else:
            otf = self.otf_attenuated_array if attenuated else self.otf_array
        return shift_otf(otf, kx, ky)

    def _load_otf(self) -> None:
        kx, ky = 0, 0
        attenuation_fwhm = (
            self.sim_parameters.attenuation_fwhm
            * self.microscope_parameters.pixel_size
            * 1e-3
        )
        # 1e-3 because the input is in nm but the fwhm is for um
        if self.sim_parameters.otf_type.upper() == "FILE":
            self.otf_array = get_otf_from_file(
                self.sim_parameters.otf_file_location, self.image_parameters.image_shape
            )
        else:
            self.otf_array = get_ideal_otf_array(
                self.image_parameters.image_shape,
                self.cutoff,
                kx,
                ky,
                self.sim_parameters.otf_type.upper(),
                self.sim_parameters.otf_correction,
            )

        self.otf_attenuated_array = self.otf_array * get_attenuation_array(
            self.image_parameters.image_shape,
            self.sim_parameters.attenuation_strength,
            attenuation_fwhm,
            kx,
            ky,
        )
        return
