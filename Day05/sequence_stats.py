# To start the program, copy the following text to your OS's command window: python sequence_stats.py name_of_file.format
# Example with a file name: python sequence_stats.py a_seq.txt
# Make sure that the path is set to the directory that holds both the program file (sequence_stats.py) and the sequence file (a_seq.txt).

import argparse
import os
from collections import Counter

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def calculate_statistics(sequence):
    length=len(sequence)
    char_count=Counter(sequence.upper())
    
    actg_sum=sum(char_count[char] for char in "ACTG")
    percentage={char:(char_count[char]/actg_sum*100) if actg_sum>0 else 0 for char in "ACTG"}

    unknown_count=length-actg_sum
    percentage["Unknown"]=(unknown_count/length*100) if length>0 else 0
    char_count["Unknown"]=unknown_count
    
    return {"total":length, "character_count":char_count, "percentages":percentage}

def display_statistics(file_name, stats):
    print(file_name)

    for char in "ACTG":
        count=stats["character_count"].get(char, 0)
        percentage=stats["percentages"].get(char, 0)
        print(f"{char}:        {count}   {percentage:.2f}%")

    unknown_count=stats["character_count"].get("Unknown", 0)
    unknown_percentage=stats["percentages"].get("Unknown", 0)
    print(f"Unknown:  {unknown_count}   {unknown_percentage:.2f}%")

    print("Total:   ", stats["total"])

def main():
    parser=argparse.ArgumentParser(description="Displays some basic statistics about sequences.")
    parser.add_argument("files", nargs='+', help="File(s) with sequences.")

    args=parser.parse_args()

    for file_path in args.files:
        if not os.path.isfile(file_path):
            print(f"Error: {file_path} is not a valid file.")
            continue

        sequence=read_file(file_path)
        if sequence:
            stats=calculate_statistics(sequence)
            display_statistics(file_path, stats)

if __name__ == "__main__":
    main()
