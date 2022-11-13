#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys

HTML_RENDERER_DIR = "html_renderer"
JS_BUNDLE = "pyinstrument/renderers/html_resources/app.js"
CSS_BUNDLE = "pyinstrument/renderers/html_resources/app.css"

if __name__ == "__main__":
    # chdir to root of repo
    os.chdir(os.path.dirname(__file__))
    os.chdir("..")

    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="force a rebuild of the bundle")

    args = parser.parse_args()

    js_source_mtime = 0
    for dirpath, dirnames, filenames in os.walk(HTML_RENDERER_DIR):
        if "node_modules" in dirnames:
            dirnames.remove("node_modules")

        for filename in filenames:
            file = os.path.join(dirpath, filename)
            js_source_mtime = max(js_source_mtime, os.path.getmtime(file))

    js_bundle_is_up_to_date = (
        os.path.exists(JS_BUNDLE) and os.path.getmtime(JS_BUNDLE) >= js_source_mtime
    )

    if js_bundle_is_up_to_date and not args.force:
        print("Bundle up-to-date")
        sys.exit(0)

    if subprocess.call("npm --version", shell=True) != 0:
        raise RuntimeError("npm is required to build the HTML renderer.")

    subprocess.check_call("npm ci", cwd=HTML_RENDERER_DIR, shell=True)
    subprocess.check_call("npm run build", cwd=HTML_RENDERER_DIR, shell=True)

    shutil.copyfile(HTML_RENDERER_DIR + "/dist/pyinstrument-html.iife.js", JS_BUNDLE)
    shutil.copyfile(HTML_RENDERER_DIR + "/dist/style.css", CSS_BUNDLE)
