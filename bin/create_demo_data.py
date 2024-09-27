#!/usr/bin/env python3

import os
import subprocess
import sys
from glob import glob
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def main():
    os.chdir(ROOT_DIR)
    for script in glob(str("examples/demo_scripts/*.py")):
        subprocess.run([sys.executable, "bin/create_sample_json.py", script], check=True)


if __name__ == "__main__":
    main()
