"""
Outputs first name frequencies from partial Pile data.

A better name for this file would be count_partial_pile.py
"""
from collections import Counter
import sys
import pandas
import datetime
import pathlib
import argparse
import jsonlines
import json
import tqdm
import lm_dataformat as lmd


def get_length(reader):
    count = 0
    for _ in catch_json_error(reader.stream_data()):
        count += 1
    return count


def get_names_set(min_freq=110_000):
    # I choose min_frequency of name manually. I chose this threshold to have reasonable/diverse names
    # while still excluding "my" (100,000 count apparently).
    name_path = pathlib.Path("analysis_world_name_frequency.csv")
    df = pandas.read_csv(name_path)
    mask = df.nobs >= min_freq
    return set(df[mask].name)


NAMES_SET = get_names_set()


def catch_json_error(generator):
    try:
        yield from generator
    except jsonlines.jsonlines.InvalidLineError:
        pass


def main2():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=pathlib.Path)
    parser.add_argument("--output_dir", type=pathlib.Path)
    args = parser.parse_args()

    reader = lmd.Reader(str(args.input_file))
    length = get_length(reader)

    cnt = Counter()
    for text in tqdm.tqdm(catch_json_error(reader.stream_data()), total=length):
        for word in text.split():
            word: str
            if len(word) <= 1:
                continue
            if not word[0].isupper():
                continue
            if not word.isascii():
                continue
            if word.lower() not in NAMES_SET:
                continue

            chars = set(word)
            banned_chars = set("<>")
            if len(chars.intersection(banned_chars)) > 0:
                continue

            drop_suffixes = ".,!?"
            if word[-1] in drop_suffixes:
                word = word[:-1]
            cnt[word.lower()] += 1

    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        filename = str(args.input_file).replace("/", "__") + "_names.json"
        output_path = args.output_dir / filename
        with open(output_path, "w") as f:
            json.dump(dict(cnt), f)
        print(f"Wrote counts of {len(cnt)} unique words to {output_path}", file=sys.stderr)
    else:
        print(json.dumps(dict(cnt)))


if __name__ == "__main__":
    main2()
