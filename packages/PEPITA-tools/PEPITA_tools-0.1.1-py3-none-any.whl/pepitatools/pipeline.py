# Imports
# Standard Library Imports
import copy
import json
import math
import os
from pathlib import Path
import re
from time import time
import warnings

# External Imports
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Local Imports
from . import absolute, analyze, dose_response, interactions, utils
from .configuration import get_config_setting

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMS = [str(n) for n in range(1, 99)]


def adjust_absolute_filename(filename):
    filepath = Path(filename)
    return filepath.parent.joinpath(filepath.stem + "_absolute" + filepath.suffix)


def generate_plate_schematic(
    schematic,
    results,
    conversions=None,
    plate_info="[Unknown]",
    scale=None,
    well_count=96,
    cmap="mako",
    max_val=100,
):
    results = copy.deepcopy(results)  # don't mess with `results`, it's used after this

    # scale values, and adjust heatmap settings accordingly, if necessary

    if scale is not None:
        min_, max_ = scale
        for solution, values in results.items():
            for i in range(len(values)):
                values[i] = (values[i] - min_) / (max_ - min_)

    vmax, hmap_fmt, cbar_fmt, cbar_label = (
        (
            1,
            ".0%",
            PercentFormatter(xmax=1, decimals=0),
            "Remaining Hair-Cell Brightness",
        )
        if scale is not None
        else (max_val, ".0f", None, "Pipeline Score")
    )

    # produce matrix of responses by combining data from `schematic` and `results`

    # iterate backwards so as not to mess up indices for subsequent loops
    for row_idx in reversed(range(len(schematic))):
        if not schematic[row_idx]:
            del schematic[
                row_idx
            ]  # remove empty lists or numpy will reject ragged array

    height = len(schematic)
    max_width = max([len(schematic[row_idx]) for row_idx in range(height)])

    annotations = np.full((height, max_width), "", dtype=object)
    responses = np.full((height, max_width), np.nan, dtype=np.double)

    for row_idx in range(height):
        for col_idx in range(len(schematic[row_idx])):
            solution = utils.Solution(schematic[row_idx][col_idx], conversions)
            result = results[solution].pop(0)
            label = re.sub(
                r"([A-Z])([A-Za-z])\w+\s?([\d./]+)?([A-Za-zμ ]+)?",
                lambda m: f'{m.group(1)}{m.group(2).lower()}{m.group(3) if m.group(3) else ""}',
                schematic[row_idx][col_idx],
            )
            label = re.sub(r"\s+", "", label)
            label = re.sub(r"\+", "+\n", label)
            annotations[row_idx, col_idx] = f"{result:{hmap_fmt}}\n{label}"
            responses[row_idx, col_idx] = result

    plate_height = utils.plate_height(well_count)
    plate_width = well_count // plate_height

    col_labels = NUMS[1 : plate_width - 1]
    row_labels = list(ALPHA[1 : plate_height - 1])

    plates_count_est = math.ceil(len(responses) / plate_height)

    row_labels *= plates_count_est

    for i in range(
        plates_count_est - 1, 0, -1
    ):  # insert blank line(s) for any plates > 1
        insertable_idx = (len(responses) // plates_count_est) * i
        annotations = np.insert(
            annotations, insertable_idx, np.full_like(annotations[0], ""), axis=0
        )
        responses = np.insert(
            responses, insertable_idx, np.full_like(responses[0], np.nan), axis=0
        )
        row_labels = row_labels[0:insertable_idx] + [""] + row_labels[insertable_idx:]

    # make the heatmap

    _fig = plt.figure(figsize=(12, 6 * plates_count_est), dpi=100)

    ax = sns.heatmap(
        responses,
        vmin=0,
        vmax=vmax,
        cmap=cmap,
        annot=annotations,
        fmt="",
        linewidths=2,
        square=True,
        cbar_kws={
            "format": cbar_fmt,
            "label": cbar_label,
            "ticks": [0, vmax],
        },
        xticklabels=col_labels,
        yticklabels=row_labels,
    )
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    if max_val < 100:
        suffix1, suffix2 = ", Log", "_log"
    elif scale is None:
        suffix1, suffix2 = "", ""
    elif scale[1] > 10_000:
        suffix1, suffix2 = ", Absolute", "_absolute"
    else:
        suffix1, suffix2 = ", Scaled", "_scaled"

    plt.title(f"{plate_info} {well_count}-well Plate Schematic{suffix1}")
    uniq_str = str(int(time() * 1000) % 1_620_000_000_000)
    log_dir = f'{get_config_setting("log_dir")}/dose_response'
    plt.savefig(
        f"{log_dir}/{plate_info}_{well_count}-well_schematic_heatmap{suffix2}_{uniq_str}.png"
    )
    plt.clf()


def main(
    imagefiles,
    cap=-1,
    chartfile=None,
    checkerboard=False,
    conversions=None,
    debug=0,
    group_regex=".*",
    platefile=None,
    plate_control=None,
    plate_ignore=None,
    plate_info=None,
    plate_positive_control=None,
    treatment_platefile=None,
    absolute_chart=False,
    silent=False,
    talk=False,
):
    if conversions is None:
        conversions = []
    if plate_control is None:
        plate_control = ["B"]
    if plate_ignore is None:
        plate_ignore = []
    if plate_positive_control is None:
        plate_positive_control = []
    hashfile = utils.get_inputs_hashfile(
        imagefiles=imagefiles,
        cap=cap,
        group_regex=group_regex,
        platefile=platefile,
        plate_control=plate_control,
        plate_ignore=plate_ignore,
    )

    if talk:
        sns.set_context("talk")

    conversions = dict(conversions)
    schematic = analyze.get_schematic(
        platefile, len(imagefiles), plate_ignore, flat=False
    )

    if absolute_chart:
        abs_chartfile = adjust_absolute_filename(chartfile)
        results2 = absolute.main(
            imagefiles,
            cap=cap,
            chartfile=abs_chartfile,
            debug=0,
            group_regex=group_regex,
            platefile=platefile,
            plate_control=plate_control,
            plate_ignore=plate_ignore,
            silent=False,
        )
        results2 = {
            utils.Solution(key, conversions): value for key, value in results2.items()
        }
        abs_max = int(get_config_setting("absolute_max_ototox"))
        abs_min = int(get_config_setting("absolute_min_ototox"))
        generate_plate_schematic(
            schematic,
            results2,
            conversions=conversions,
            plate_info=plate_info,
            scale=(abs_min, abs_max),
            well_count=96,
        )

    if chartfile is None and debug == 0 and os.path.exists(hashfile):
        with open(hashfile, "r") as f:  # read cached results
            results = json.load(f)
    else:
        results = analyze.main(
            imagefiles,
            cap,
            chartfile,
            debug,
            group_regex,
            platefile,
            plate_control,
            plate_ignore,
            silent=False,
        )
        with open(hashfile, "w") as f:  # cache results for reuse
            json.dump(results, f)

    drug_conditions = _parse_results(results, conversions)
    control_drugs = [
        utils.Cocktail(utils.Dose(control).drug) for control in plate_control
    ]
    models = {}

    results = {
        utils.Solution(key, conversions): value for key, value in results.items()
    }

    # positive control

    positive_control_solutions = [
        utils.Solution(positive_control, conversions)
        for positive_control in plate_positive_control
    ]
    positive_control_scores = [
        result
        for solution in positive_control_solutions
        for result in results[solution]
    ]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        positive_control_value = np.nanmean(positive_control_scores)

    if np.isnan(positive_control_value):
        print(
            (
                "WARNING: No positive control included. Using minimum calculated value as "
                "positive control"
            )
        )
        positive_control_value = np.nanmin(
            [value for condition, values in results.items() for value in values]
        )

    # generate plate schematics

    generate_plate_schematic(
        schematic,
        results,
        conversions=conversions,
        plate_info=plate_info,
        scale=(positive_control_value, 100),
        well_count=96,
    )

    # generate models, dose-response charts

    for cocktail, conditions in drug_conditions.items():
        if cocktail in control_drugs:
            continue
        cocktail_scores = {}
        summary_scores = []
        for control_drug in control_drugs:
            for solution in drug_conditions[control_drug]:
                conditions.insert(0, solution)
        for solution in conditions:
            cocktail_scores[solution] = results[solution]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                summary_score = np.nanmedian(results[solution])
                summary_scores.append(summary_score)
        models[cocktail] = dose_response.Model(
            conditions, summary_scores, cocktail, E_max=positive_control_value
        )
        models[cocktail].chart(
            results[solution],
            datapoints=cocktail_scores,
            name=plate_info + "_" + str(cocktail) if plate_info else None,
            scale=[positive_control_value, 100],
        )

    # print EC values

    for model in models.values():
        for ec_value in (50, 75, 90, 99):
            concentn = model.effective_concentration(ec_value / 100)
            if not np.isnan(concentn):
                print(
                    (
                        f"{model.get_condition()} "
                        f"EC_{ec_value}={concentn:.2f}{model.get_x_units()}"
                    )
                )

    # analyze combinations

    models_combo = [model for model in models.values() if model.combo]

    if not checkerboard:
        total_max_x = 1
        total_max_y = 1

        fig = plt.figure(figsize=(12, 8), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.margins(0.006)

        for model_combo in models_combo:
            subcocktail_a = utils.Cocktail(model_combo.cocktail.drugs[0])
            if subcocktail_a not in models:
                continue
            subcocktail_b = utils.Cocktail(model_combo.cocktail.drugs[1])
            model_a = models[subcocktail_a]
            model_b = models[subcocktail_b]
            plot_filename, max_x, max_y = dose_response.analyze_diamond(
                model_a, model_b, model_combo
            )
            dose_response.chart_diamond(model_a, model_b, model_combo)

            total_max_x = max(total_max_x, max_x)
            total_max_y = max(total_max_y, max_y)

        if models_combo and plot_filename is not None:
            plt.xlim(right=total_max_x)
            plt.ylim(top=total_max_y)
            plt.savefig(plot_filename)
            plt.close()
            plt.clf()
    else:
        pairs = {
            (model_combo.cocktail.drugs[0], model_combo.cocktail.drugs[1])
            for model_combo in models_combo
        }

        for pair in pairs:
            model_a, model_b = (
                models[utils.Cocktail(pair[0])],
                models[utils.Cocktail(pair[1])],
            )

            models_combo_relevant = [
                model_combo
                for model_combo in models_combo
                if model_combo.cocktail.drugs[0] in pair
                and model_combo.cocktail.drugs[1] in pair
            ]

            dose_response.analyze_checkerboard(
                model_a,
                model_b,
                models_combo_relevant,
                method="Bliss",
                file_name_context=plate_info,
            )
            dose_response.chart_checkerboard(
                model_a, model_b, models_combo_relevant, file_name_context=plate_info
            )

            doses_a = np.array(
                [x.doses[0] for x in model_a.xs if x.get_drugs() != ("Control",)]
            )
            doses_b = np.array(
                [x.doses[0] for x in model_b.xs if x.get_drugs() != ("Control",)]
            )

            responses_all_a = squarify(
                [results[x] for x in model_a.xs if x.get_drugs() != ("Control",)]
            )
            responses_all_b = squarify(
                [results[x] for x in model_b.xs if x.get_drugs() != ("Control",)]
            )

            combo_solutions = [
                solution for solution in results.keys() if len(solution.doses) > 1
            ]

            doses_a_ab = np.array([solution.doses[0] for solution in combo_solutions])
            doses_b_ab = np.array([solution.doses[1] for solution in combo_solutions])
            responses_all_ab = squarify(
                [results[solution] for solution in combo_solutions]
            )

            if not positive_control_scores:
                positive_control_scores = np.array(
                    [
                        min(
                            [
                                result
                                for results_list in results.values()
                                for result in results_list
                            ]
                        )
                    ]
                )

            if not plate_info:
                plate_info = os.path.basename(
                    os.path.dirname(os.path.dirname(imagefiles[0]))
                )

            try:
                interactions.response_surface(
                    doses_a,
                    responses_all_a,
                    doses_b,
                    responses_all_b,
                    doses_a_ab,
                    doses_b_ab,
                    responses_all_ab,
                    positive_control_scores,
                    sampling_iterations=1000,
                    sample_size=20,
                    model_size=1,
                    alpha=0.1,
                    file_name_context=plate_info,
                )
            except ValueError as ve:
                if ve.args[0] == "cov must be 2 dimensional and square":
                    print("Unable to analyze non-square interaction matrix")
                else:
                    raise ve


def squarify(list_of_lists):
    width = max([len(row) for row in list_of_lists])

    for row in list_of_lists:
        pad_size = width - len(row)
        row.extend([np.nan for _ in range(pad_size)])

    return np.array(list_of_lists)


def _key_value_pair(argument, delimiter="="):
    return tuple(argument.split(delimiter))


def _parse_results(results, conversions):
    drug_conditions = {}
    for condition in results:
        solution = utils.Solution(condition, conversions)
        utils.put_multimap(drug_conditions, solution.get_cocktail(), solution)
    return drug_conditions
