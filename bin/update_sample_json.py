#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.session import Session

ROOT_DIR = Path(__file__).parent.parent
OUTPUT_FILE = ROOT_DIR / "html_renderer" / "public" / "sample.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("SESSION_FILE", help="The session file to load")
    args = parser.parse_args()
    session = Session.load(args.SESSION_FILE)

    with open(OUTPUT_FILE, "w") as f:
        renderer = HTMLRenderer()
        f.write(renderer.render_json(session))

    print(f"Sample JSON written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
