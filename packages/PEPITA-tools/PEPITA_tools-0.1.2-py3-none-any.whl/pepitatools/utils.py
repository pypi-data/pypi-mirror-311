"""
Utility functions for PEPITA-tools
"""

# Imports
# Standard Library Imports
from __future__ import annotations
import base64
import hashlib
import math
import os
import pickle
import re

# External Imports
import numpy as np

# Local Imports
from .configuration import get_config_setting


class Cocktail:
    def __eq__(self, other):
        return self.drugs == other.drugs and self.ratio == other.ratio

    def __hash__(self):
        return hash(self.drugs) ^ hash(self.ratio)

    def __init__(self, drugs, effect=None, ratio=None):
        self.drugs = drugs if not isinstance(drugs, str) else (drugs,)
        self.effect = effect
        self.ratio = ratio

    def __repr__(self):
        string = "+".join(self.drugs)
        if self.ratio:
            string += f"@{self.ratio}"
            if (
                self.effect
            ):  # effect level only relevant if ratio is set, otherwise confusing
                string += f"(EC{self.effect})"
        return string


class Dose:
    _ec_pattern = re.compile(r"([0-9]*)([A-Z]{3}[0-9]{2})/?([0-9]*)")
    _vector_pattern = re.compile(r"(.+?) ([0-9]+[.]?[0-9]*) ?([^0-9]+)")

    def __add__(self, other):
        return Dose(f"{self.drug} {self.quantity + float(other)}{self.unit}")

    def __eq__(self, other):
        if not isinstance(other, Dose):
            return False
        return (
            self.drug == other.drug
            and self.quantity == other.quantity
            and self.unit == other.unit
        )

    def __float__(self):
        return self.quantity

    def __hash__(self):
        return hash(self.drug) ^ hash(self.quantity) ^ hash(self.unit)

    def __init__(self, string, conversions=None):
        if conversions is None:
            conversions = {}

        self.converted = False
        self.ec = False
        self.string = string

        ec_match = Dose._ec_pattern.fullmatch(string)

        if ec_match:
            self.ec = True
            multiplier, ec_data, divisor = ec_match.group(1, 2, 3)
            self.series = ec_data
            if ec_data in conversions:
                self.converted = True
                ec_data = conversions[ec_data]
            vector_match = Dose._vector_pattern.fullmatch(ec_data)
        elif string in conversions:
            vector_match = Dose._vector_pattern.fullmatch(conversions[string])
            self.converted = True
            self.series = None
            multiplier, divisor = None, None
        else:
            vector_match = Dose._vector_pattern.fullmatch(string)
            self.series = None
            multiplier, divisor = None, None

        if vector_match:
            self.drug, self.quantity, self.unit = vector_match.group(1, 2, 3)
            self.quantity = float(self.quantity)
            if not self.series:
                self.series = vector_match.group(1)
        else:
            raise ValueError(
                f'Dose string "{string}" unknown or not in the proper format'
            )

        if multiplier:
            self.quantity *= int(multiplier)
        if divisor:
            self.quantity /= int(divisor)

    def __mul__(self, other):
        return Dose(f"{self.drug} {self.quantity * other}{self.unit}")

    def __radd__(self, other):
        return Dose(f"{self.drug} {float(other) + self.quantity}{self.unit}")

    def __repr__(self):
        return f"{self.drug} {self.quantity}{self.unit}"


class Ratio:
    def __eq__(self, other):
        if isinstance(other, Ratio):
            return (self.num * other.denom) == (other.num * self.denom)
        else:
            return float(self) == float(other)

    def __float__(self):
        return self.num / self.denom

    def __hash__(self):
        return hash(round(self.num / self.denom, 8))

    def __init__(self, num, denom):
        self.num = num
        self.denom = denom

    def __mul__(self, other):
        return round(other * self.num / self.denom, 8)

    def __rmul__(self, other):
        return round(other * self.num / self.denom, 8)

    def __repr__(self):
        return f"{self.num}:{self.denom}"

    def __rtruediv__(self, other):
        return other * self.reciprocal()

    def reciprocal(self):
        return Ratio(self.denom, self.num)

    def to_proportion(self):
        return Ratio(self.num, self.num + self.denom)


class Solution:
    def __init__(self, string, conversions=None):
        if conversions is None:
            conversions = []

        self.conversions = conversions
        self.string = string
        dose_strings = [s.strip() for s in string.split("+")]
        self.doses = [Dose(string, conversions) for string in dose_strings]

    def __eq__(self, other):
        if not isinstance(other, Solution):
            return False
        return self.doses == other.doses

    def __float__(self):
        return float(sum(self.doses))

    def __gt__(self, other):
        return float(self) > float(other)

    def __hash__(self):
        return hash(tuple(self.doses))

    def __mul__(self, other):
        doses = [dose * other for dose in self.doses]
        return Solution(" + ".join([dose.string for dose in doses]))

    def __repr__(self):
        return "+".join(
            f"{dose.drug} {dose.quantity}{dose.unit}" for dose in self.doses
        )

    def __rmul__(self, other):
        return other * float(self)

    def __truediv__(self, other):
        return float(self) / other

    def combine_doses(self, other):
        return Solution(f"{self.string} + {other.string}")

    def dilute(self, dilution):
        if dilution < 0 or dilution > 1:
            raise ValueError("Solution should be diluted by a factor between 0 and 1")
        doses = [dose * dilution for dose in self.doses]
        return Solution(" + ".join([dose.string for dose in doses]))

    def get_cocktail(self):
        effect = extract_number(self.doses[0].series)
        return Cocktail(
            tuple(dose.drug for dose in self.doses),
            effect=(None if np.isnan(effect) else effect),
            ratio=(None if len(self.doses) != 2 else self.ratio()),
        )

    def get_drugs(self):
        return tuple(dose.drug for dose in self.doses)

    def get_units(self):
        return "+".join(str(dose.unit) for dose in self.doses)

    def ratio(self):
        if len(self.doses) == 2:
            return Ratio(self.doses[0].quantity, self.doses[1].quantity)
        raise ValueError(f"This solution {self.doses} does not have a valid dose ratio")

    def reverse(self):
        doses = self.doses[::-1]
        return Solution(" + ".join([str(dose) for dose in doses]), self.conversions)


def equalsish(val1, val2, delta=0.001):
    return abs(val1 - val2) < delta


def extract_number(string):
    number_match = re.search(r"[0-9.]+", string)
    if number_match:
        return float(number_match.group(0))
    else:
        return np.nan


def geometric_mean(array):
    return np.exp(np.mean(np.log(array)))


# def get_config(setting, fallback=None):
# 	global _config
# 	if _config == None:
# 		_config = configparser.ConfigParser()
# 		_config.read(f'{get_here()}/config.ini')
# 		_config.read(f'{get_here()}/config-ext.ini')
# 	return _config[_section].get(setting, fallback)


def get_inputs_hashfile(**kwargs):
    sha1hash = hashlib.sha1()
    for value in kwargs.values():
        sha1hash.update(pickle.dumps(value))
    digest = base64.b32encode(sha1hash.digest()).decode("utf-8")
    os.makedirs(os.path.join(get_config_setting("log_dir"), ".cache"), exist_ok=True)
    return os.path.join(get_config_setting("log_dir"), ".cache", f".{digest}.json")


def plate_height(well_count):
    sqrt = int(math.sqrt(well_count))

    for i in range(sqrt, 1, -1):
        if well_count % i == 0:
            return i

    print(f"WARNING: proper plate height not found for {well_count}-well plate")
    return sqrt


def put_multimap(dict_, key, value):
    list_ = dict_.get(key, [])
    list_.append(value)
    dict_[key] = list_


def remove_argument(parser, arg):
    removed = False

    for action in parser._actions:
        if (
            action.option_strings and arg in action.option_strings
        ) or action.dest == arg:
            parser._remove_action(action)
            removed = True
            break

    for action in parser._action_groups:
        for group_action in action._group_actions:
            if group_action.dest == arg:
                action._group_actions.remove(group_action)
                removed = True
                break

    return removed


def remove_arguments(parser, *args):
    return [remove_argument(parser, arg) for arg in args]
