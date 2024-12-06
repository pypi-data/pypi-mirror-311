"""
Main CLI for pepita-tools
"""

# Imports
# Standard library imports
from __future__ import annotations
import argparse
import json
import os
import sys
from time import time
import warnings

# External imports
from matplotlib import pyplot as plt
import numpy as np


# Local Imports
from pepitatools import (
    analyze,
    absolute,
    dose_response,
    imagej_scripts,
    imageops,
    infection,
    keyence,
    pipeline,
    utils,
)
from pepitatools.configuration import (
    read_config,
    get_config_setting,
    set_config_setting,
    _DEFAULT_CONFIG_STR,
)


def set_arguments(parser):
    parser.add_argument(
        "imagefiles",
        nargs="+",
        help="The absolute or relative filenames where the relevant images can be found.",
    )
    parser.add_argument(
        "-ch",
        "--chartfile",
        help="If supplied, the resulting numbers will be charted at the given filename.",
    )

    parser.add_argument(
        "-p",
        "--platefile",
        help="CSV file containing a schematic of the plate from which the given images were "
        "taken. Row and column headers are optional. The cell values are essentially just "
        "arbitrary labels: results will be grouped and charted according to the supplied "
        "values.",
    )
    parser.add_argument(
        "-pc",
        "--plate-control",
        default=["B"],
        nargs="*",
        help=(
            "Labels to treat as the control condition in the plate schematic. These wells are "
            "used to normalize all values in the plate for more interpretable results. Any number "
            "of values may be passed."
        ),
    )
    parser.add_argument(
        "-pi",
        "--plate-ignore",
        default=[],
        nargs="*",
        help=(
            "Labels to ignore (treat as null/empty) in the plate schematic. Empty cells will "
            'automatically be ignored, but any other null values (e.g. "[empty]") must be '
            "specified here. Any number of values may be passed."
        ),
    )

    parser.add_argument(
        "-g",
        "--group-regex",
        default=".*",
        help=(
            "Pattern to be used to match group names that should be included in the results. "
            "Matched groups will be included, groups that don't match will be ignored. Control "
            "wells will always be included regardless of whether they match."
        ),
    )

    parser.add_argument(
        "-c",
        "--cap",
        default=-1,
        type=int,
        help=(
            "Exclude well values larger than the given integer, expressed as a percentage of "
            "the median control value."
        ),
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help=(
            "Indicates intermediate processing images should be output for troubleshooting "
            "purposes. Including this argument once will yield one intermediate image per input "
            "file, twice will yield several intermediate images per input file."
        ),
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help=(
            "If present, printed output will be suppressed. More convenient for programmatic "
            "execution."
        ),
    )


# region Merge Config and Command Line Options
def merge_config_cli(args):
    """Take in command line arguments, and update the configuration based on them"""
    if args.absolute_max_infection:
        set_config_setting("absolute_max_infection", args.absolute_max_infection)
    if args.absolute_min_infection:
        set_config_setting("absolute_min_infection", args.absolute_min_infection)
    if args.absolute_max_ototox:
        set_config_setting("absolute_max_ototox", args.absolute_max_ototox)
    if args.absolute_min_ototox:
        set_config_setting("absolute_min_ototox", args.absolute_min_ototox)
    if args.channel_main_ototox:
        set_config_setting("channel_main_ototox", args.channel_main_ototox)
    if args.channel_main_infection:
        set_config_setting("channel_main_infection", args.channel_main_infection)
    if args.channel_subtr_ototox:
        set_config_setting("channel_subtr_ototox", args.channel_subtr_ototox)
    if args.channel_subtr_infection:
        set_config_setting("channel_subtr_infection", args.channel_subtr_infection)
    if args.filename_replacement_delimiter:
        set_config_setting(
            "filename_replacement_delimiter", args.filename_replacement_delimiter
        )
    if args.filename_replacement_brightfield_infection:
        set_config_setting(
            "filename_replacement_brightfield_infection",
            args.filename_replacement_brightfield_infection,
        )
    if args.filename_replacement_brightfield_ototox:
        set_config_setting(
            "filename_replacement_brightfield_ototox",
            args.filename_replacement_brightfield_ototox,
        )
    if args.filename_replacement_mask_infection:
        set_config_setting(
            "filename_replacement_mask_infection",
            args.filename_replacement_mask_infection,
        )
    if args.filename_replacement_mask_ototox:
        set_config_setting(
            "filename_replacement_mask_ototox", args.filename_replacement_mask_ototox
        )
    if args.filename_replacement_subtr_infection:
        set_config_setting(
            "filename_replacement_subtr_infection",
            args.filename_replacement_subtr_infection,
        )
    if args.filename_replacement_subtr_ototox:
        set_config_setting(
            "filename_replacement_subtr_ototox", args.filename_replacement_subtr_ototox
        )
    if args.log_dir:
        set_config_setting("log_dir", args.log_dir)
    if args.keyence_lenses_file:
        set_config_setting("keyence_lenses_file", args.keyence_lenses_file)


# endregion Merge Config and Command Line Options


# region subcommands
def config_file_command(args):
    if args.directory is None:
        directory = os.getcwd()
    else:
        directory = args.directory
    with open(os.path.join(directory, "config.ini"), "w") as f:
        f.write(_DEFAULT_CONFIG_STR)


def keyence_file_command(args):
    if args.directory is None:
        directory = os.getcwd()
    else:
        directory = args.directory
    keyence.write_example(os.path.join(directory, "keyence_lenses.csv"))


def absolute_command(args):
    args_dict = vars(args)
    absolute.main(**args_dict)


def analyze_command(args):
    args_dict = vars(args)
    analyze.main(**args_dict)


def keyence_command(args):
    for filename in args.filenames:
        metadata = keyence.extract_metadata(filename)
        print(filename, json.dumps(metadata, indent=2))


def imageops_command(args):
    for bf_filename in args.imagefiles:
        fl_filename = bf_filename.replace("CH4", "CH1")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            bf_img = imageops.read(bf_filename, np.uint16)
            fl_img = (
                None if not args.particles else imageops.read(fl_filename, np.uint16, 1)
            )
        imageops.get_fish_mask(
            bf_img,
            fl_img,
            particles=args.particles,
            silent=args.debug < 1,
            verbose=args.debug > 1,
            v_file_prefix="imageops",
            mask_filename=bf_filename.replace("CH4", "mask"),
        )


def dose_response_command(args):
    if args.filename is None:
        models = [dose_response._get_neo_model(debug=0)]
    else:
        models = [dose_response._get_model(f) for f in args.filename]
    colors = ["#def", "#cdf", "#bcf", "#abf", "#9af", "#89f", "#78f"]

    for i, model in enumerate(models):
        print(model.cocktail)
        ec_90 = model.effective_concentration(0.9)
        ec_75 = model.effective_concentration(0.75)
        ec_50 = model.effective_concentration(0.5)

        print(f"E_max: {model.get_absolute_E_max()} score")
        print(f"EC_90: {ec_90} μM")
        print(f"ec_75: {ec_75} μM")
        print(f"ec_50: {ec_50} μM")

        model.chart(close=False, color=colors[i])

    plt.xlabel(f"{models[0].get_condition()} Dose (μM)")
    plt.ylabel("Pipeline Score")

    uniq_str = str(int(time() * 1000) % 1_620_000_000_000)
    plt.savefig(
        os.path.join(
            get_config_setting("log_dir"), f"{models[0].get_condition()}_{uniq_str}.png"
        )
    )
    plt.close()
    plt.clf()


def infection_command(args):
    args_dict = vars(args)
    try:
        infection.main(**args_dict)
    except analyze.UserError as ue:
        print("Error:", ue)
        sys.exit(1)


def pipeline_command(args):
    args_dict = vars(args)
    try:
        pipeline.main(**args_dict)
    except analyze.UserError as ue:
        print("Error:", ue)
        sys.exit(1)


def imagej_scripts_command(args):
    if args.scripts is None:
        scripts = [
            "openformasking",
            "openformaskingsingle",
            "savefishmask",
            "savefishnullmask",
            "macroize",
        ]
    else:
        scripts = args.scripts
    for script in scripts:
        imagej_scripts.write_script(script, args.directory)


# endregion subcommands


def create_parser():
    # region toplevel parser
    top_parser = argparse.ArgumentParser(prog="PEPITA-tools")
    top_parser.add_argument(
        "--config",
        dest="config",
        required=False,
        default="./config.ini",
        help="Path to config file, if not provided will look for config.ini in current "
        "directory",
    )

    # Add arguments which will be suppressed, but which can override the config file
    top_parser.add_argument(
        "--absolute_max_infection",
        dest="absolute_max_infection",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--absolute_min_infection",
        dest="absolute_min_infection",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--absolute_max_ototox",
        dest="absolute_max_ototox",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--absolute_min_ototox",
        dest="absolute_min_ototox",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--channel_main_ototox",
        dest="channel_main_ototox",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--channel_main_infection",
        dest="channel_main_infection",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--channel_subtr_ototox",
        dest="channel_subtr_ototox",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--channel_subtr_infection",
        dest="channel_subtr_infection",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--filename_replacement_delimiter",
        dest="filename_replacement_delimiter",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--filename_replacement_brightfield_infection",
        dest="filename_replacement_brightfield_infection",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--filename_replacement_brightfield_ototox",
        dest="filename_replacement_brightfield_ototox",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--filename_replacement_mask_infection",
        dest="filename_replacement_mask_infection",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--filename_replacement_mask_ototox",
        dest="filename_replacement_mask_ototox",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--filename_replacement_subtr_infection",
        dest="filename_replacement_subtr_infection",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--filename_replacement_subtr_ototox",
        dest="filename_replacement_subtr_ototox",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--log_dir",
        dest="log_dir",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )
    top_parser.add_argument(
        "--keyence_lenses_file",
        dest="keyence_lenses_file",
        required=False,
        default=None,
        help=argparse.SUPPRESS,
    )

    subparsers = top_parser.add_subparsers(help="Subcommands", required=True)
    top_parser.set_defaults(command=None)
    # endregion toplevel parser

    # region config-file parser
    # Create the parse for the "config-file" command
    config_file_parser = subparsers.add_parser(
        "config-file", help="Create a default config file"
    )
    config_file_parser.add_argument(
        "-d",
        "--directory",
        required=False,
        default=None,
        type=str,
        help="Directory to place default config file, current directory is used if not provided",
    )
    config_file_parser.set_defaults(func=config_file_command, command="config-file")
    # endregion config-file parser

    # region keyence-file parser
    keyence_file_parser = subparsers.add_parser(
        "keyence-file", help="Create a default keyence lenses file"
    )
    keyence_file_parser.add_argument(
        "-d",
        "--directory",
        required=False,
        default=None,
        type=str,
        help="Directory to place default config file, "
        "current directory is used if not provided",
    )
    keyence_file_parser.set_defaults(func=keyence_file_command, command="keyence-file")
    # endregion keyence-file parser

    # region absolute parser
    # Create the parser for the absolute script
    absolute_parser = subparsers.add_parser(
        "absolute",
        help="Analyzer for images of whole zebrafish with stained neuromasts, for the "
        "purposes of measuring hair cell damage in absolute terms. Reports values in "
        "arbitrary units not relative to any other value.",
    )
    set_arguments(absolute_parser)
    absolute_parser.set_defaults(func=absolute_command)
    # endregion absolute parser

    # region analyze parser
    # Create the parser for the Analyze Script
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyzer for images of whole zebrafish with stained "
        "neuromasts, for the purposes of measuring hair cell damage."
        " Reports values relative to control.",
    )
    set_arguments(analyze_parser)
    analyze_parser.set_defaults(func=analyze_command)
    # endregion analyze parser

    # region keyence
    # Create the Parser for the keyence script
    keyence_parser = subparsers.add_parser(
        "keyence", help="Print the metadata from keyence files"
    )
    keyence_parser.add_argument(
        "filenames", nargs="+", help="Files to get metadata from"
    )
    keyence_parser.set_defaults(func=keyence_command)

    # Create the parser for the imageops command
    imageops_parser = subparsers.add_parser(
        "imageops",
        help="Utility for operating on images of whole zebrafish with stained neuromasts, "
        "for the purposes of measuring hair cell damage.",
    )
    imageops_parser.add_argument(
        "imagefiles",
        nargs="+",
        help="The absolute or relative filenames where the relevant images can be found.",
    )
    imageops_parser.add_argument(
        "-p",
        "--particles",
        action="store_true",
        help=(
            "If present, the resulting mask will obscure everything except the bright particles "
            "on the fish in the given images. Otherwise the whole fish will be shown."
        ),
    )
    imageops_parser.add_argument(
        "-d",
        "--debug",
        action="count",
        default=1,
        help=(
            "Indicates intermediate processing images should be output for troubleshooting "
            "purposes. Including this argument once will yield one intermediate image per input "
            "file, twice will yield several intermediate images per input file."
        ),
    )
    imageops_parser.set_defaults(func=imageops_command)
    # endregion keyence

    # region dose_response parser
    # Create the parser for the dose_response script
    dose_response_parser = subparsers.add_parser(
        name="dose_response", help="Evaluate the dose response for different models"
    )
    dose_response_parser.add_argument(
        "filename",
        nargs="*",
        default=None,
        help="filenames containing dose response models",
    )
    dose_response_parser.set_defaults(func=dose_response_command)

    # endregion dose_response parser

    # region infection parser
    infection_parser = subparsers.add_parser(
        name="infection",
        help=(
            "Analyzer for images of whole zebrafish with stained neuromasts, for the "
            "purposes of measuring hair cell damage under drug-combination conditions. Reports "
            "values relative to control."
        ),
    )

    infection_parser.add_argument(
        "-cb",
        "--checkerboard",
        action="store_true",
        help=(
            "If present, the input will be treated as a checkerboard assay, with output produced "
            "accordingly."
        ),
    )

    infection_parser.add_argument(
        "-cv",
        "--conversions",
        default=[],
        nargs="*",
        type=infection._key_value_pair,
        help=(
            "List of conversions between dose concentration labels and concrete values, each as "
            "a separate argument, each delimited by an equals sign. For instance, ABC50 might be "
            "an abbreviation for the EC50 of drug ABC, in which case the concrete concentration "
            'can be supplied like "ABC50=ABC 1mM" (make sure to quote, or escape spaces).'
        ),
    )

    infection_parser.add_argument(
        "-ppc",
        "--plate-positive-control",
        default=[],
        nargs="*",
        help=(
            "Labels to treat as the positive control conditions in the plate schematic (i.e. "
            "conditions showing maximum effect). These wells are used to normalize all values in "
            "the plate for more interpretable results. Any number of values may be passed."
        ),
    )

    infection_parser.add_argument(
        "--plate-info",
        default=None,
        help=(
            "Any information identifying the plate(s) being analyzed that should be passed along "
            "to files created by this process."
        ),
    )

    infection_parser.add_argument(
        "-tp",
        "--treatment-platefile",
        help="CSV file containing a schematic of the plate in which the imaged fish were treated. "
        "Used to chart responses by treatment location, if desired. Row and column headers are "
        "optional. The cell values are essentially just arbitrary labels: results will be "
        "grouped and charted according to the supplied values.",
    )

    infection_parser.add_argument(
        "--absolute-chart",
        action="store_true",
        help=(
            "If present, a plate graphic will be generated with absolute (rather than relative) "
            "brightness values."
        ),
    )

    infection_parser.add_argument(
        "--talk",
        action="store_true",
        help=('If present, images will be generated with the Seaborn "talk" context.'),
    )
    set_arguments(infection_parser)
    utils.remove_arguments(infection_parser, "plate_ignore", "group_regex")
    infection_parser.set_defaults(func=infection_command)

    # endregion infection parser

    # region pipeline parser
    pipeline_parser = subparsers.add_parser(
        "pipeline",
        help=(
            "Analyzer for images of whole zebrafish with fluorescent neuromasts, for the "
            "purposes of measuring hair cell damage under drug-combination conditions. Reports "
            "values relative to control."
        ),
    )
    pipeline_parser.add_argument(
        "-cb",
        "--checkerboard",
        action="store_true",
        help=(
            "If present, the input will be treated as a checkerboard assay, with output produced "
            "accordingly."
        ),
    )

    pipeline_parser.add_argument(
        "-cv",
        "--conversions",
        default=[],
        nargs="*",
        type=pipeline._key_value_pair,
        help=(
            "List of conversions between dose concentration labels and concrete values, each as "
            "a separate argument, each delimited by an equals sign. For instance, ABC50 might be "
            "an abbreviation for the EC50 of drug ABC, in which case the concrete concentration "
            'can be supplied like "ABC50=ABC 1mM" (make sure to quote, or escape spaces).'
        ),
    )

    pipeline_parser.add_argument(
        "-ppc",
        "--plate-positive-control",
        default=[],
        nargs="*",
        help=(
            "Labels to treat as the positive control conditions in the plate schematic (i.e. "
            "conditions showing maximum effect). These wells are used to normalize all values in "
            "the plate for more interpretable results. Any number of values may be passed."
        ),
    )

    pipeline_parser.add_argument(
        "--plate-info",
        default=None,
        help=(
            "Any information identifying the plate(s) being analyzed that should be passed along "
            "to files created by this process."
        ),
    )

    pipeline_parser.add_argument(
        "-tp",
        "--treatment-platefile",
        help="CSV file containing a schematic of the plate in which the imaged fish were treated. "
        "Used to chart responses by treatment location, if desired. Row and column headers are "
        "optional. The cell values are essentially just arbitrary labels: results will be "
        "grouped and charted according to the supplied values.",
    )

    pipeline_parser.add_argument(
        "--absolute-chart",
        action="store_true",
        help=(
            "If present, a plate graphic will be generated with absolute (rather than relative) "
            "brightness values."
        ),
    )

    pipeline_parser.add_argument(
        "--talk",
        action="store_true",
        help=(
            'If present, images will be generated with the Seaborn "talk" context. Otherwise the '
            'default "notebook" context will be used. (See '
            "https://seaborn.pydata.org/generated/seaborn.set_context.html)"
        ),
    )
    set_arguments(pipeline_parser)
    pipeline_parser.set_defaults(func=pipeline_command)

    # endregion pipeline parser

    # region imagej scripts parser
    script_parser = subparsers.add_parser(
        "imagej-script", help="Write ImageJ scripts to provided directory"
    )
    script_parser.add_argument(
        "scripts",
        nargs="*",
        default=None,
        help="Names of scripts to write to 'directory', if not provided will save all scripts "
        "to directory.",
    )
    script_parser.add_argument(
        "-d",
        "--directory",
        default=".",
        help="Path (relative or absolute) to directory to write Imagej scripts, if not "
        "provided will save scripts to current directory",
        dest="directory",
    )
    script_parser.set_defaults(func=imagej_scripts_command)
    # endregion imagej scripts parser

    return top_parser


def pepita():
    # Create Parser
    parser = create_parser()
    # Parse arguments from stdin
    args = parser.parse_args()
    if (args.command != "config-file") and (args.command != "keyence-file"):
        # Read the config file
        read_config(args.config)
        # Replace default config with passed command line arguments
        merge_config_cli(args)
    # Call the desired subcommand
    args.func(args)


if __name__ == "__main__":
    pepita()
