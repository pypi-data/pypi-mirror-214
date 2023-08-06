import logging
from typing import Union, Optional, Dict

logger = logging.getLogger(__name__)

SI_PREFIXES = {
    "Y": 1e24,
    "Z": 1e21,
    "E": 1e18,
    "P": 1e15,
    "T": 1e12,
    "G": 1e9,
    "M": 1e6,
    "k": 1e3,
    "h": 1e2,
    "da": 1e1,
    "d": 1e-1,
    "c": 1e-2,
    "m": 1e-3,
    "u": 1e-6,
    "µ": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
    "a": 1e-18,
    "z": 1e-21,
    "y": 1e-24,
}

SI_UNITS = ["m", "kg", "s", "A", "K", "mol", "cd", "1"]


def to_SI(a: Union[float, Dict], unit: Optional[str] = None) -> float:
    """converts the value with unit to the base SI unit"""
    if type(a) == dict:
        unit = a["unit"]
        value = a["value"]
    else:
        value = a
    if "/" in unit:
        nominator, denominator = unit.split("/")
    else:
        nominator = unit
        denominator = ""
    # resolve nominator
    value *= parse_unit_chain(nominator)
    value /= parse_unit_chain(denominator)
    return value


def parse_unit_chain(chain: str) -> float:
    """parses a string of space seperated units.
    returns the factor for conversion to base units."""
    if len(chain) == 0:
        return 1
    conv_factor = 1
    for single_unit in chain.split(
        " "
    ):  # single units need to be spaced so mK /= m K has a clear meaning
        if single_unit in SI_UNITS:  # unit already present as base unit
            continue
        elif single_unit[1:] in SI_UNITS:
            conv_factor *= SI_PREFIXES[single_unit[0]]
        elif single_unit[2:] in SI_UNITS:  # for the case of da which has 2 letters
            conv_factor *= SI_PREFIXES[single_unit[0:2]]
        else:
            raise ValueError(
                f"{single_unit} is not in the supported format for a unit."
            )
    return conv_factor
