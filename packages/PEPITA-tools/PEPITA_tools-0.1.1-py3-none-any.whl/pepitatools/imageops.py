"""
Image Operation Functions
"""

# Imports
# Standard Library Imports
from __future__ import annotations

import os
import pathlib
from time import time
import warnings

# External Imports
import cv2 as cv
import imageio
import numpy as np
from skimage import feature


# Local Imports
from .configuration import get_config_setting


def apply_mask(img, mask):  # mask should have black background, white foreground
    img_type = _get_bit_depth(img)
    return np.minimum(img, np.where(mask == 255, img_type[1], 0).astype(img_type[0]))


def binarize(img, threshold):
    if threshold >= 0:
        return np.where(img < threshold, 255, 0).astype(np.uint8)
    else:
        return img


def circle_local_maxima(img, count=50, discard=0, min_pct=0.05, radius=8):
    coordinates = _get_local_maxima(
        img, count=count + discard, spacing=radius, threshold_rel=min_pct
    )
    maxima = np.zeros_like(img)
    for coordinate in coordinates[discard:]:
        maxima[coordinate[0]][coordinate[1]] = 255
    return dilate(maxima, size=radius)


def close(img, size=1, iterations=1):
    if size > 0 and iterations > 0:
        return cv.morphologyEx(
            img, cv.MORPH_CLOSE, _get_kernel(size), iterations=iterations
        )
    else:
        return img


def dilate(img, size=1, iterations=1):
    if size > 0 and iterations > 0:
        return cv.dilate(img, _get_kernel(size), iterations=iterations)
    else:
        return img


def erode(img, size=1, iterations=1):
    if size > 0 and iterations > 0:
        return cv.erode(img, _get_kernel(size), iterations=iterations)
    else:
        return img


def get_aspect_mask(img, target_ratio=5, error_bound=0.5):
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    upper, lower = target_ratio * (1 + error_bound), target_ratio / (1 + error_bound)
    contours = [
        contour for contour in contours if _aspect_is_between(contour, upper, lower)
    ]
    return cv.drawContours(
        np.ones(img.shape, dtype=np.uint8) * 255, contours, -1, (0, 255, 0), cv.FILLED
    )


def get_contours_by_area(img, threshold=-1, lower=0, upper=2**32):
    binarized_img = binarize(img, threshold)
    contours, _ = cv.findContours(binarized_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    areas = np.array([cv.contourArea(contour) for contour in contours])
    return [contour for contour, area in zip(contours, areas) if lower < area < upper]


def get_fish_mask(
    bf_img,
    fl_img,
    particles=True,
    silent=True,
    verbose=False,
    v_file_prefix="",
    mask_filename=None,
    subtr_img=None,
):
    if subtr_img is None:
        subtr_img = []
    show(
        bf_img,
        verbose=verbose or not silent,
        v_file_prefix=v_file_prefix,
    )
    show(
        fl_img,
        verbose=verbose or not silent,
        v_file_prefix=v_file_prefix,
    )

    if subtr_img is not None and len(subtr_img) > 0:
        fl_img = subtract(fl_img, subtr_img, scale=True)
        show(
            fl_img,
            verbose=verbose or not silent,
            v_file_prefix=v_file_prefix,
        )

    if mask_filename and os.path.isfile(mask_filename):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            mask_img = read(mask_filename, np.uint8)
            show(mask_img, verbose=verbose, v_file_prefix=v_file_prefix)

        if particles:
            steps = (
                lambda img_i: apply_mask(fl_img, mask_img),
                lambda img_i: circle_local_maxima(
                    img_i, count=10, discard=5, min_pct=0.05, radius=8
                ),
            )
        else:
            steps = (lambda img_i: mask_img,)
    else:
        steps = (
            rescale_brightness,
            lambda img_i: binarize(img_i, threshold=2**14),
            lambda img_i: apply_mask(
                img_i,
                get_size_mask(
                    bf_img,
                    erosions=10,
                    threshold=2**12,
                    lower=2**15,
                    verbose=verbose,
                    v_file_prefix=v_file_prefix,
                ),
            ),
            lambda img_i: close(img_i, size=6, iterations=16),
            lambda img_i: dilate(img_i, size=5, iterations=6),
            lambda img_i: get_size_mask(
                img_i,
                erosions=4,
                threshold=-1,
                lower=2**15,
                upper=2**19,
                verbose=verbose,
                v_file_prefix=v_file_prefix,
            ),
            invert,
        )
        if particles:
            steps = (
                *steps,
                lambda img_i: apply_mask(fl_img, img_i),
                lambda img_i: circle_local_maxima(
                    img_i, count=10, discard=5, min_pct=0.05, radius=8
                ),
            )

    mask = _get_mask(bf_img, steps, verbose=verbose, v_file_prefix=v_file_prefix)
    show(
        apply_mask(fl_img, mask),
        verbose=not verbose and not silent,
        v_file_prefix=v_file_prefix,
    )
    return mask


def get_size_mask(
    img,
    erosions=0,
    threshold=2**7,
    lower=0,
    upper=2**32,
    verbose=False,
    v_file_prefix="",
):
    contours = get_contours_by_area(img, threshold, lower, upper)
    steps = (
        lambda img_i: cv.drawContours(
            np.ones(img_i.shape, dtype=np.uint8) * 255,
            contours,
            -1,
            (0, 255, 0),
            cv.FILLED,
        ),
        lambda img_i: erode(img_i, size=4, iterations=erosions),
    )
    return _get_mask(img, steps, verbose=verbose, v_file_prefix=v_file_prefix)


def invert(img):
    return np.subtract(_get_bit_depth(img)[1], img)


def read(filename, target_bit_depth, channel=-1):
    img = imageio.v2.imread(filename)
    if channel >= 0:
        img = img[:, :, channel]

    bit_depth = _get_bit_depth(img)
    if bit_depth[0] != target_bit_depth:
        img = (img * (np.iinfo(target_bit_depth).max / bit_depth[1])).astype(
            target_bit_depth
        )

    return img


def rescale_brightness(img):
    img_type = _get_bit_depth(img)
    return ((img - img.min()) * (img_type[1] / img.max())).astype(img_type[0])


def resize(img, factor):
    return cv.resize(img, None, fx=factor, fy=factor)


def score(img, count=10, radius=8, threshold_pct=0.05):
    coordinates = _get_local_maxima(img, count=count, spacing=radius)
    height, width = img.shape
    total = 0

    for coord_y, coord_x in coordinates:
        x_min, x_max = (
            max(coord_x - radius, 0),
            min(coord_x + radius, width),
        )  # bounding box
        y_min, y_max = max(coord_y - radius, 0), min(coord_y + radius, height)  #
        points = []
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                if (x - coord_x) ** 2 + (
                    y - coord_y
                ) ** 2 > radius**2:  # Pythagorean theorem
                    continue
                points.append(img[y][x])
        relevant_points = sorted(points, reverse=True)[
            : int(len(points) * threshold_pct)
        ]
        total += sum(relevant_points)
    return total


def setup_imageops_logdir():
    base_log_dir = get_config_setting("log_dir")
    if base_log_dir == "/path/to/log/dir":
        raise ValueError(
            (
                "Your log_dir configuration is not set. Please provide a log_dir value in config-ext.ini "
                "so this package knows where to write relevant files. See "
                "https://github.com/ma-lab-cgidr/PEPITA-tools?tab=readme-ov-file#configuration-file "
                "for more details."
            )
        )
    log_dir = pathlib.Path(f"{base_log_dir}/imageops")
    if not log_dir.exists():
        try:
            os.makedirs(log_dir, exist_ok=True)
        except OSError as ose:
            raise ValueError(
                (
                    "Your log_dir configuration points to a location that can't be properly written to. See "
                    "https://github.com/ma-lab-cgidr/PEPITA-tools?tab=readme-ov-file#configuration-file "
                    "for details on configurations, and see the chained error for more details on the specific "
                    "problem."
                )
            ) from ose
    return log_dir


def show(img, verbose=True, v_file_prefix=""):
    if verbose:
        log_dir = setup_imageops_logdir()
        unique_str = str(int(time() * 1000) % 1_620_000_000_000)
        filename = f"{log_dir}/{v_file_prefix}_{unique_str}.png"
        imageio.imwrite(filename, resize(img, 0.5))


# NOTE: at the moment, it's assumed minuend_image and subtrahend_image have the same bit depth
def subtract(minuend_image, subtrahend_image, scale=True, threshold=0.005):
    if scale:
        threshold_px = _get_bit_depth(minuend_image)[1] * threshold
        intersection_mask = (minuend_image > threshold_px) & (
            subtrahend_image > threshold_px
        )
        minuend_masked_median = np.median(minuend_image[intersection_mask])
        subtrahend_masked_median = np.median(subtrahend_image[intersection_mask])
        scaled_image = subtrahend_image * (
            minuend_masked_median / subtrahend_masked_median
        )
        subtrahend_image = scaled_image.astype(subtrahend_image.dtype)
    # subtract without underflow
    return np.where(
        minuend_image < subtrahend_image, 0, minuend_image - subtrahend_image
    )


def _aspect_is_between(contour, upper, lower):
    _, (minor, major), _ = cv.fitEllipse(contour)
    aspect_ratio = major / minor
    return (aspect_ratio < upper) and (aspect_ratio > lower)


def _get_bit_depth(img):
    types = [(itype, np.iinfo(itype).max) for itype in [np.uint8, np.uint16, np.int32]]
    return types[np.digitize(img.max(), [itype[1] for itype in types], right=True)]


def _get_kernel(size):
    return cv.getStructuringElement(
        cv.MORPH_ELLIPSE, (size * 2 + 1, size * 2 + 1), (size, size)
    )


def _get_local_maxima(img, count=10, spacing=5, threshold_rel=0.1):
    return feature.peak_local_max(
        img, min_distance=spacing, num_peaks=count, threshold_rel=threshold_rel
    )


def _get_mask(img, steps, verbose=False, v_file_prefix=""):
    img_i = img
    for step in steps:
        img_i = step(img_i)
        show(img_i, verbose, v_file_prefix=v_file_prefix)
    show(apply_mask(img, img_i), verbose, v_file_prefix=v_file_prefix)
    return img_i
