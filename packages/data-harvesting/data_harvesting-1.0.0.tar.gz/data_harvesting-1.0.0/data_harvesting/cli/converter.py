# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Cli converter command to convert between different rdf formats and enrich them"""
from pathlib import Path
from typing import List

import typer
from rdflib import Graph
from rdflib.compare import graph_diff
from rich.console import Console

from data_harvesting.util.json_ld_util import convert
from data_harvesting.util.json_ld_util import valdiate_from_file

console = Console()
app = typer.Typer(add_completion=True)


@app.command('diff')
def diff(  #avoid name conflict
    filename1: Path,
    filename2: Path,
    in_format1: str = typer.Option('json-ld', '--out-format', '-of', help='The format of file1'),
    in_format2: str = typer.Option('json-ld', '--in-format', '-if', help='The format of fifle2')) -> None:
    """Convert given files to specified format using rdflib

    full example usage
    ```
    hmc_unhide rdf convert --out_format ttl --in_format json-ld --destination ./out_ttl ./dir/*.json
    ```
    """
    graph1 = Graph()
    graph1.parse(filename1, format=in_format1)

    graph2 = Graph()
    graph2.parse(filename2, format=in_format2)

    in_both, in_first, in_second = graph_diff(graph1, graph2)
    print('Only in second:')
    for sub, pre, obj in in_second:
        print(f'{sub} , {pre} , {obj}')
    print('\n Only in first:')
    for sub, pre, obj in in_first:
        print(f'{sub} , {pre} , {obj}')

    print('\n In both:')
    for sub, pre, obj in in_both:
        print(f'{sub} , {pre} , {obj}')


@app.command('convert')
def _convert(  #avoid name conflict
    filenames: List[Path],
    destination: Path = typer.Option(
        Path('.'), '-o', help='The output folder to save the files, or in the case of a single file, the new name.'),
    out_format: str = typer.Option('ttl', '--out-format', '-of', help='The format to convert to'),
    in_format: str = typer.Option('json-ld', '--in-format', '-if', help='The format to convert from')) -> None:
    """Convert given files to specified format using rdflib

    full example usage
    ```
    hmc_unhide rdf convert --out_format ttl --in_format json-ld --destination ./out_ttl ./dir/*.json
    ```
    """
    # todo move this somewhere else
    format_suffix_map = {'json-ld': 'jsonld'}

    for filename in filenames:
        if destination.is_dir():
            name = filename.name.rstrip(filename.suffix)
            # convert out format to sufix...
            suffix = format_suffix_map.get(out_format, out_format)
            destfilepath = destination / Path(f'{name}.{suffix}')
        else:
            destfilepath = destination
        print(f'Converting {filename} to {out_format} and saving to {destfilepath}')
        convert(filename, destfilepath=destfilepath, informat=in_format, outformat=out_format, overwrite=False)


@app.command()
def validate(
    filenames: List[Path],
    format_f: str = typer.Option('jsonld', '--format', help='The format of the inputfile(s) if not jsonld'),
) -> None:
    """Validate given file(s), default format jsonld, shacl validation against unhide/schema.org

    format could be, jsonld, json, unhide, ttl...
    full example usage
    ```
    hmc_unhide rdf validate --format jsonld ./*.json
    ```
    """
    for filename in filenames:
        print(f'Validating {filename}')
        res, validator = valdiate_from_file(filename)
        print(res)
        if res:
            print(f'This file is valid: {filename}')
