#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = ROOT_DIR / "html_renderer" / "demo-data"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("SCRIPT", help="The script to run to produce the sample", type=Path)
    args = parser.parse_args()
    script_file: Path = args.SCRIPT
    output_file = (OUTPUT_DIR / script_file.with_suffix("").name).with_suffix(".json")

    result = subprocess.run(
        [
            "pyinstrument",
            "-o",
            str(output_file),
            "-r",
            "pyinstrument.renderers.html.JSONForHTMLRenderer",
            script_file,
        ]
    )

    if result.returncode != 0:
        return result.returncode

    print(f"Sample JSON written to {output_file}")


if __name__ == "__main__":
    sys.exit(main())
