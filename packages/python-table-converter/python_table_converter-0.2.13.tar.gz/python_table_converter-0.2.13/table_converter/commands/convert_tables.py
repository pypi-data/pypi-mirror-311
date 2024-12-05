# -*- coding: utf-8 -*-

import argparse

from icecream import ic

from .. core.convert import convert

def run(
    args: argparse.Namespace,
):
    convert(
        input_files = args.input_files,
        output_file = args.output_file,
        config_path = args.config,
        assign_constants = args.assign_constants,
        assign_formats = args.assign_formats,
        str_filters = args.filters,
        pickup_columns= args.pickup_columns,
        fields_to_split_by_newline = args.split_by_newline,
        fields_to_assign_ids = args.assign_ids,
        str_omit_fields= args.omit_fields,
        output_debug = args.output_debug,
    )

def setup_parser(
    parser: argparse.ArgumentParser,
):
    parser.add_argument(
        'input_files',
        metavar='INPUT_FILE',
        nargs='+',
        help='Path to the input file.'
    )
    parser.add_argument(
        '--output-file', '-o',
        metavar='OUTPUT_FILE',
        required=True,
        help='Path to the output file.'
    )
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to the configuration file.',
    )
    parser.add_argument(
        '--pickup-columns',
        type=str,
        help='Pickup column map',
    )
    parser.add_argument(
        '--split-by-newline',
        type=str,
        help='Fields to split by newline',
    )
    parser.add_argument(
        '--assign-ids',
        type=str,
        help='Field to assign ids',
    )
    parser.add_argument(
        '--assign-constants',
        type=str,
        help='Field to assign constants',
    )
    parser.add_argument(
        '--assign-formats',
        type=str,
        help='Field to assign formats',
    )
    parser.add_argument(
        '--filters', '--filter', '-f',
        type=str,
        help='Expression list to filter records',
    )
    parser.add_argument(
        '--omit-fields', '--omit',
        type=str,
        help='Field to omit',
    )
    parser.add_argument(
        '--output-debug',
        action='store_true',
        help='Output debug information',
    )
    parser.set_defaults(handler=run)
