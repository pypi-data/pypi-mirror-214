import logging
from typing import Optional, List

import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)


class Direction:
    def __init__(self, number_bands: int, number_phases: int) -> None:
        if number_bands < 2:
            raise RuntimeError(f"bands ({number_bands}) < 2, not usefull")
        if number_phases < (number_bands * 2 - 1):
            raise RuntimeError(
                f"not enough phases for bands: {number_bands} {number_phases}"
            )
        self.number_bands = number_bands  # how many bands
        self.number_phases = number_phases  # how many phases
        self.px, self.py = -1, -1  # shift vector (band1)
        self.phase_offset = 0  # global phase offsets ToDo
        self.phases = np.zeros(number_phases)  # phases
        self.modulations = np.ones(number_bands)  # modulation
        self.has_individual_phases = False  # if non-equidist. phases are set
        self.angle_intensity_factor = 1  # the intensity factor to apply to this angle
        self.phase_intensity_factors = np.ones(
            number_phases
        )  # the intensity factors to apply phase-by-phase
        self.reset_phases(1)  # inits the phases to equidistant
        self.mod_low_limit = 0.4
        self.mod_high_limit = 1.1
        self.default_modulation = 0.65

    def reset_phases(self, multiplier: Optional[float] = 1.0) -> None:
        """
        Reset individual phases back to equidistant.
        """
        for i in range(self.number_phases):
            self.phases[i] = (2 * np.pi * multiplier / self.number_phases) * i
            # if self.phases[i] > np.pi:
            #    self.phases[i] -= 2 * np.pi
        self.has_individual_phases = False

    def set_px_py(self, in_px: float, in_py: float) -> None:
        self.px = in_px / (self.number_bands - 1)
        self.py = in_py / (self.number_bands - 1)

    def set_phase_offset(self, phase: float):
        self.reset_phases()
        self.phase_offset = phase

    def get_intensity_quotient(self, phase: int) -> float:
        """
        Returns a combined correction quotient: 1/(angleIntesity*phaseIntensity)
        """
        return 1 / (self.angle_intensity_factor * self.phase_intensity_factors[phase])

    def get_number_of_components(self) -> int:
        return self.number_bands * 2 - 1

    def get_phases(self) -> npt.ArrayLike:
        ret = []
        for i in range(self.number_phases):
            ret.append(self.phases[i] + self.phase_offset)
        return ret

    def get_modulations(self) -> List[float]:
        ret = [x for x in self.modulations]
        for band in range(self.number_bands):
            if ret[band] < self.mod_low_limit:
                logger.warning(
                    f"Modulation {ret[band]} below limit {self.mod_low_limit}! Modulation was set to default {self.default_modulation} instead"
                )
                ret[band] = self.default_modulation
            if ret[band] > self.mod_high_limit:
                logger.warning(
                    f"Modulation {ret[band]} above limit {self.mod_high_limit}! Modulation was set to default {self.default_modulation} instead"
                )
                ret[band] = self.default_modulation
        return ret

    def as_dict(self) -> dict:
        out_dict = {}
        out_dict["number_bands"] = self.number_bands
        out_dict["number_phases"] = self.number_phases
        out_dict["px"] = self.px
        out_dict["py"] = self.py
        out_dict["phases"] = self.get_phases()
        out_dict["modulations"] = self.get_modulations()
        out_dict["angle_intensity_factor"] = self.angle_intensity_factor
        out_dict["phase_intensity_factors"] = self.phase_intensity_factors

        return out_dict

    @classmethod
    def as_descriptive_dict(cls) -> dict:
        out_dict = {}
        out_dict["number_bands"] = "Number of bands"
        out_dict["number_phases"] = "Number of phases in the image data"
        out_dict["px"] = "x component of the shift vector"
        out_dict["py"] = "y component of the shift vector"
        out_dict["phases"] = "Phase offsets of the different phases (images)"
        out_dict["modulations"] = "Modulations"
        out_dict[
            "angle_intensity_factor"
        ] = "Factor to multiply the input data from this angel"
        out_dict[
            "phase_intensity_factors"
        ] = "Factors to multiply the different phases with"

        return out_dict

    @classmethod
    def from_dict(cls, data_dict: dict) -> "Direction":
        direction = Direction(data_dict["number_bands"], data_dict["number_phases"])
        direction.px = data_dict["px"]
        direction.py = data_dict["py"]
        direction.phases = data_dict["phases"]
        direction.modulations = data_dict["modulations"]
        direction.angle_intensity_factor = data_dict["angle_intensity_factor"]
        direction.phase_intensity_factors = data_dict["phase_intensity_factors"]

        return direction
