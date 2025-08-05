import argparse
import os
import sys
import json
from dataclasses import dataclass

from PIL.Image import composite
from process_bigraph import Composite

from pbsew.core_construction import construct_core

@dataclass
class ProgramArguments:
    input_pbif_json: str
    interval: float

def get_program_arguments() -> ProgramArguments:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='BioSimulators Experiment Wrapper (BSew)',
        description='''BSew is a BioSimulators project designed to serve as a template/wrapper for 
running Process Bigraph Experiments.''')
    parser.add_argument('input_pbif_json')  # positional argument
    parser.add_argument('-n', '--interval', default=1.0, type=float)
    args = parser.parse_args()
    input_file = os.path.abspath(os.path.expanduser(args.input_pbif_json))
    if not os.path.isfile(input_file):
        print("error: `input_file_path` must be a JSON/PBIF file that exists!", file=sys.stderr)
        sys.exit(11)
    return ProgramArguments(input_file, args.interval)

def main():
    prog_args = get_program_arguments()
    with open(prog_args.input_pbif_json) as input_data:
        schema = json.load(input_data)
    core = construct_core()
    prepared_composite = Composite(core=core, config=schema)
    prepared_composite.run(prog_args.interval)

if __name__ == "__main__":
    main()
