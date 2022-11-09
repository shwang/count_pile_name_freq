# First Name Frequency Counting
You will need at least 20GB of disk space. (This is a streaming script, so doesn't store the entire Pile corpus).
```
pip install pandas jsonlines tqdm lm-dataformat
./run_all.sh  # Calls load.py on multiple JSON, outputting to script_output/
python merge_json_counts.py script_output/* > merged_counts.json
```

