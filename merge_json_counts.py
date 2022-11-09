from collections import Counter
import json

import argparse
import pathlib

def _load_json(path: pathlib.Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def merge_counts(counters: dict) -> Counter:
    result = Counter()
    for cnt in counters:
        result.update(cnt)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="+")
    args = parser.parse_args()

    counts = [_load_json(path) for path in args.filenames]
    merged_cnts = merge_counts(counts)
    str = json.dumps(merged_cnts)
    print(str)


if __name__ == "__main__":
    main()