#!/usr/bin/python
# Author: James Ross (jar35@st-andrews.ac.uk)
# 24/6/2015
#
# This script takes a record directory (containing "birth_records",
# "marriage_records", "death_records") in TD format and outputs a corrupt
# version of the records.

from datetime import datetime
import os
import sys
from populations_crptr.config import Config

def main(filepath):
    # Check input directory exists and is a directory
    if not os.path.exists(filepath):
        print(f"Directory not found: {filepath}")
        return
    
    if not os.path.isdir(filepath):
        print(f"Error: {filepath} is not a directory")
        return

    print (f"Running crptr for {filepath}")

    # Generate output directory
    now = datetime.now()
    timestamp_str = f"{now.strftime('%Y-%m-%dT%H-%M-%S')}-{now.microsecond // 1000:03d}"
    output_filepath = f"{Config.OUTPUT_DIR}/{Config.PURPOSE}/{timestamp_str}"
    os.makedirs(f"{output_filepath}/records", exist_ok=True)

    # Generate logfile path
    log_filepath = f"{output_filepath}/{Config.PURPOSE}{timestamp_str}.log"
    # Corrupts files
    files = ["birth_records.csv", "marriage_records.csv", "death_records.csv"]
    corrupt_file(filepath, output_filepath, files[0], log_filepath, Config.CORRUPTORS.birthCorruptor)
    corrupt_file(filepath, output_filepath, files[1], log_filepath, Config.CORRUPTORS.marriageCorruptor)
    corrupt_file(filepath, output_filepath, files[2], log_filepath, Config.CORRUPTORS.deathCorruptor)

    print(f"Results output to {output_filepath}")

def corrupt_file(input_dir, output_dir, filename, log_filepath, corruptor_fn):
    start_time = datetime.now()

    # Checks input file exists
    input_filepath = f"{input_dir}/{filename}"
    if not os.path.exists(input_filepath):
        print (f"Skipping, file not found: {input_filepath}")
        return

    print_timestamp(f"Corrupting {input_filepath}...")

    corruptor_fn(
        input_filepath,
        f"{output_dir}/records/{filename}",
        log_filepath,
        Config.LOOKUP_FILES_DIR,
        Config.DETERMINISTIC,
        Config.SEED,
        Config.PROFILE.PROPORTION_TO_CORRUPT,
        Config.PROFILE.MAX_MODIFICATIONS_PER_ATTR,
        Config.PROFILE.MODIFICATIONS_PER_RECORD,
        Config.PROFILE.RECORD_LEVEL_PROPORTION
    )

    print_time_elapsed(start_time)

def print_timestamp(string):
    now = datetime.now()
    print(f"{now.strftime('%Y/%m/%d %H-%M-%S')}.{now.microsecond // 1000:03d} :: ", end="")
    print(string)

def print_time_elapsed(start_time):
    elapsed = datetime.now() - start_time

    hours, remainder = divmod(elapsed.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = elapsed.microseconds // 1000

    print(f"Elapsed time: {int(hours):02}-{int(minutes):02}-{int(seconds):02}-{milliseconds:03}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python population_corruptor.py <filepath>")
    else:
        main(sys.argv[1])