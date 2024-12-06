"""
Analyze plates
"""

# Imports
# Standard Library Imports
from __future__ import annotations
import csv
import os
import re
import sys
import warnings


# External Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Local Imports
from . import imageops
from . import keyence
from .configuration import get_config_setting

# for windows consoles (e.g. git bash) to work properly
try:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass  # sys.stdout has been wrapped, but should already support utf-8


class Image:
    def __init__(
        self,
        filename,
        group,
        debug=0,
    ):
        # Get values from config
        self.channel = int(get_config_setting("channel_main_ototox"))
        self.channel_subtr = int(get_config_setting("channel_subtr_ototox"))
        self.particles = True
        self.replacement_delim = get_config_setting("filename_replacement_delimiter")
        self.replacement_brfld = get_config_setting(
            "filename_replacement_brightfield_ototox"
        ).split(self.replacement_delim)
        self.replacement_mask = get_config_setting(
            "filename_replacement_mask_ototox"
        ).split(self.replacement_delim)
        self.replacement_subtr = get_config_setting(
            "filename_replacement_subtr_ototox"
        ).split(self.replacement_delim)
        self.fl_filename = filename
        self.bf_filename = filename.replace(
            self.replacement_brfld[0], self.replacement_brfld[1]
        )
        self.subtr_filename = filename.replace(
            self.replacement_subtr[0], self.replacement_subtr[1]
        )

        match = re.search(r"([a-zA-Z0-9]+)_XY([0-9][0-9])_", filename)
        if not match:
            raise UserError("Filename %s missing needed xy information" % filename)

        self.plate = match.group(1)
        self.xy = int(match.group(2))

        self.group = group
        self.debug = debug

        self.bf_img = None
        self.bf_metadata = None
        self.fl_img = None
        self.fl_metadata = None
        self.subtr_img = None
        self.mask = None
        self.normalized_value = None
        self.value = None

    def get_bf_img(self):
        if self.bf_img is None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                self.bf_img = imageops.read(self.bf_filename, np.uint16)
        return self.bf_img

    def get_bf_metadata(self):
        if self.bf_metadata is None:
            self.bf_metadata = keyence.extract_metadata(self.bf_filename)
        return self.bf_metadata

    def get_fl_img(self):
        if self.fl_img is None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                self.fl_img = imageops.read(self.fl_filename, np.uint16, self.channel)
        return self.fl_img

    def get_fl_metadata(self):
        if self.fl_metadata is None:
            self.fl_metadata = keyence.extract_metadata(self.fl_filename)
        return self.fl_metadata

    def get_mask(self):
        if self.mask is None:
            self.mask = imageops.get_fish_mask(
                self.get_bf_img(),
                self.get_fl_img(),
                particles=self.particles,
                silent=self.debug < 1,
                verbose=self.debug >= 2,
                v_file_prefix="{}_XY{:02d}".format(self.plate, self.xy),
                mask_filename=self.fl_filename.replace(
                    self.replacement_mask[0], self.replacement_mask[1]
                ),
                subtr_img=self.get_subtr_img(),
            )
        return self.mask

    def get_raw_value(self):
        if self.value is None:
            fl_img_masked = imageops.apply_mask(self.get_fl_img(), self.get_mask())
            score = imageops.score(fl_img_masked)
            self.value = score if score > 0 else np.nan
        return self.value

    def get_subtr_img(self):
        if self.subtr_img is None:
            if os.path.isfile(self.subtr_filename):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    self.subtr_img = imageops.read(
                        self.subtr_filename, np.uint16, self.channel_subtr
                    )
            else:
                self.subtr_img = []
        return self.subtr_img

    def normalize(self, control_values, cap):
        try:
            val = float(self.get_raw_value() * 100 // control_values[self.plate])
            if cap > 0:
                self.normalized_value = val if val < cap else np.nan
            else:
                self.normalized_value = val
        except ZeroDivisionError:
            print(
                "ERROR: Plate",
                self.plate,
                "group",
                self.group,
                "with value",
                self.get_raw_value(),
                "has control value",
                control_values[self.plate],
            )
            self.normalized_value = np.nan
        return self


class UserError(ValueError):
    pass


def chart(results, chartfile, scale="linear"):
    with sns.axes_style(style="whitegrid"):
        data = pd.DataFrame(
            {
                "brightness": [
                    value for values in results.values() for value in values
                ],
                "group": [key for key, values in results.items() for _ in values],
            }
        )

        _fig = plt.figure(figsize=(12, 8), dpi=100)
        ax = sns.swarmplot(x="group", y="brightness", data=data)
        ax.set_yscale(scale)
        if scale == "linear":
            ax.set_ylim(bottom=0)
        sns.boxplot(
            x="group",
            y="brightness",
            data=data,
            showbox=False,
            showcaps=False,
            showfliers=False,
            whiskerprops={"visible": False},
        )
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(chartfile)


def get_schematic(platefile, target_count, plate_ignore=None, flat=True):
    if not platefile:
        return keyence.LAYOUT_DEFAULT
    if plate_ignore is None:
        plate_ignore = []

    if "" not in plate_ignore:
        plate_ignore.append("")

    with open(platefile, encoding="utf8", newline="") as f:
        schematic = [
            [well for well in row if well not in plate_ignore] for row in csv.reader(f)
        ]

    count = sum([len(row) for row in schematic])
    if (
        count != target_count
    ):  # try removing first row and first column, see if then it matches up
        del schematic[0]
        for row in schematic:
            del row[0]
        count = sum([len(row) for row in schematic])
        if count != target_count:
            raise UserError(
                f"Schematic does not have same number of cells ({count}) as images provided "
                + f"({target_count})"
            )

    return schematic if not flat else [well for row in schematic for well in row]


def quantify(
    imagefiles, plate_control=None, cap=-1, debug=0, group_regex=".*", schematic=None
):
    if plate_control is None:
        plate_control = ["B"]
    pattern = re.compile(group_regex)
    images = [
        Image(filename, group, debug)
        for filename, group in zip(imagefiles, schematic)
        if group in plate_control or pattern.search(group)
    ]
    control_values = _calculate_control_values(images, plate_control)
    return [image.normalize(control_values, cap) for image in images]


def _calculate_control_values(images, plate_control):
    ctrl_imgs = [img for img in images if img.group in plate_control]
    ctrl_vals = {}

    for plate in np.unique([img.plate for img in ctrl_imgs]):
        ctrl_results = np.array(
            [img.get_raw_value() for img in ctrl_imgs if img.plate == plate]
        )
        ctrl_vals[plate] = float(np.nanmedian(ctrl_results))

    if not ctrl_vals:
        raise UserError(
            "No control wells found. Please supply a --plate-control, or modify the given value."
        )

    return ctrl_vals


def main(
    imagefiles,
    cap=-1,
    chartfile=None,
    debug=0,
    group_regex=".*",
    platefile=None,
    plate_control=None,
    plate_ignore=None,
    silent=False,
):
    if plate_control is None:
        plate_control = ["B"]
    if plate_ignore is None:
        plate_ignore = []
    results = {}

    schematic = get_schematic(platefile, len(imagefiles), plate_ignore)
    groups = list(dict.fromkeys(schematic))  # deduplicated copy of `schematic`
    images = quantify(
        imagefiles,
        plate_control,
        cap=cap,
        debug=debug,
        group_regex=group_regex,
        schematic=schematic,
    )

    pattern = re.compile(group_regex)
    for group in groups:
        if group in plate_control or pattern.search(group):
            relevant_values = [
                img.normalized_value for img in images if img.group == group
            ]
            results[group] = relevant_values
            if not silent:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    print(group, np.nanmedian(relevant_values), relevant_values)

    if chartfile:
        chart(results, chartfile)

    return results
