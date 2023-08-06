import argparse
import json
import pathlib
from irisml.compiler import Compiler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filepath', type=pathlib.Path)
    parser.add_argument('--output_filepath', '-o', type=pathlib.Path, required=True)
    parser.add_argument('-I', action='append', dest='include_paths', default=[])

    args = parser.parse_args()

    compiler = Compiler()
    job_description = compiler.compile(args.input_filepath, args.include_paths)
    args.output_filepath.parent.mkdir(parents=True, exist_ok=True)
    args.output_filepath.write_text(json.dumps(job_description.to_dict(), indent=4) + '\n')


if __name__ == '__main__':
    main()
