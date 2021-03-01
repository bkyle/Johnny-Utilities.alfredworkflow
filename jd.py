#!/usr/bin/env python3

from typing import List, Dict
import json
import os
import subprocess
import sys

def ls(wd: str) -> List[str]:
    """Returns a list of directories under ``wd`` that match the johnny.decimal
pattern. The directories returned will be related to the passed working directory."""
    pattern = "[1234567890][1234567890]-*/[1234567890][1234567890]\ */[1234567890][1234567890].[1234567890][1234567890]*"
    cmd = ["/bin/sh", "-c", "ls -1d %s" % pattern]
    listing = subprocess.check_output(cmd, cwd=wd, text=True)
    return listing.splitlines()

def item(relpath: str , wd: str) -> Dict:
    """Returns a dict to be included in the search filer results."""
    basename = os.path.basename(relpath)
    abspath = os.path.join(wd, relpath)
    return {
        "type": "file",
        "title": basename,
        "subtitle": relpath,
        "arg": abspath,
        "icon": {
            "type": "fileicon",
            "path": abspath,
        },
    }

def main():
    wd: str = sys.argv[1] if len(sys.argv) == 2 else None
    if not wd:
        wd = os.getenv("JOHNNY_ROOT")
    if not wd:
        wd = os.getcwd()
    wd = os.path.expanduser(wd)

    results = {"items": [item(relpath, wd) for relpath in ls(wd)]}
    print(json.dumps(results))

if __name__ == "__main__":
    main()
