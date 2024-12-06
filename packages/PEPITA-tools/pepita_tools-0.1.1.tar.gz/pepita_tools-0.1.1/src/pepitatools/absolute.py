""" """

# Imports
# Standard Library Imports
from __future__ import annotations
import math
import re
import warnings

# External Imports
import numpy as np

# Local Imports
from . import analyze


# from ISO 12232:1998 via https://en.wikipedia.org/wiki/Film_speed#Measurements_and_calculations
# H = qLt/(N^2)
# H: luminous exposure (lux-seconds), proportional to pixel value
# L: luminance = variable of interest (candela/m^2)
# t: exposure time (seconds)
# N: aperture f-stop (unitless)
# q = (π/4) * T * v(θ) * cos^4(θ)
# T: transmittance of lens system (should be roughly constant for a given microscope)
# v: vignetting factor (currently ignored, could maybe be calculated from brightfield image)
# θ: angle relative to the lens
# therefore solved for L: L = H * N^2 / qt
# from https://en.wikipedia.org/wiki/Numerical_aperture#Numerical_aperture_versus_f-number
# N = f/D; NA = n * sin(arctan(D/2f))
# f: focal length of optical system
# D: diameter of entrance pupil
# NA: numerical aperture of the lens
# n: index of refraction of working medium (1.00 for air, 1.33 for water, 1.52 for immersion oil)
# therefore N in terms of NA and n: N = 1 / (2 * tan(arcsin(NA/n)))
# values are returned in units proportional to candela/m^2
def get_absolute_value(
    image, debug=0, n=1.0, transmittance=1, vignette=lambda theta: 1
):
    metadata = image.get_fl_metadata()

    H = image.get_raw_value()
    N = 1 / (2 * math.tan(math.asin(metadata["Numerical Aperture"] / n)))
    theta = 0  # TODO: calculate theta from working distance & weighted average(?) of signal in img
    q = (math.pi / 4) * transmittance * vignette(theta) * math.cos(theta) ** 4
    t = metadata["Exposure"]["Value"]

    if debug >= 1:
        print(
            '%s: H=%f "lx⋅s", N=%f, theta=%f rad, q=%f, t=%fs'
            % (image.fl_filename, H, N, theta, q, t)
        )

    L = H * N**2 / q / t

    return (
        np.nan if np.isnan(L) else int(L / 10_000)
    )  # to make results more readable, "cd/cm^2"


def main(
    imagefiles,
    cap=-1,
    chartfile=None,
    debug=0,
    group_regex=".*",
    platefile=None,
    plate_control=["B"],
    plate_ignore=[],
    silent=False,
):
    results = {}

    schematic = analyze.get_schematic(platefile, len(imagefiles), plate_ignore)
    groups = list(dict.fromkeys(schematic))  # deduplicated copy of `schematic`
    pattern = re.compile(group_regex)
    images = [
        analyze.Image(filename, group, debug)
        for filename, group in zip(imagefiles, schematic)
        if group in plate_control or pattern.search(group)
    ]

    pattern = re.compile(group_regex)
    for group in groups:
        if group in plate_control or pattern.search(group):
            relevant_values = [
                get_absolute_value(img) for img in images if img.group == group
            ]
            results[group] = relevant_values
            if not silent:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    print(group, np.nanmedian(relevant_values), relevant_values)

    if chartfile:
        analyze.chart(results, chartfile)

    return results
