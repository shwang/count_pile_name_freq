#!/bin/bash
# Downloading from the pile.
# wget 'the-eye.eu/public/AI/pile/train/##.jsonl.zst'
## varies from 00, 01, ..., 29.

set -e

data_dir=script_data
output_dir=script_output

for idx in {00..29}; do
  filename_zip="${idx}.jsonl.zst"
  url="the-eye.eu/public/AI/pile/train/${filename_zip}"
  filename="${idx}.jsonl"

  # Remove old data.
  rm -rf $data_dir

  # Download new data.
  mkdir -p $data_dir
  pushd $data_dir
  wget "$url"

  # The first and last lines are corrupted in most files,
  # since we are only doing a partial extraction. So we drop the first and last lines.
  echo "Extracting $filename_zip"
  zstdcat $filename_zip | tail -n +1 | head -n -1 > $filename
  popd

  data_path=$data_dir/$filename
  python load.py ${data_path} --output_dir $output_dir
done
