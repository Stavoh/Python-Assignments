## Read me
#
# ncbi.py is a command line tool that can download data from NCBI.
# The tool creates a new folder called "downloads" for the downloaded files.
# The date, database, search term, number asked for, and total number of items found, will be saved in a csv file called "metadata.csv".
#
# To initiate the tool with default settings, i.e. database = nucleotides, number = 10, use the following template:
# python ncbi.py  --Search_Term
# Example:
# python ncbi.py  --term iris
#
# To determine the database and/or the number, use this extended template:
# python ncbi.py  --database Name_Of_Database --term Search_Term --number Number_Of_Files_To_Download
# Example:
# python ncbi.py  --database protein --term brca1 --number 5
#
# Each item is saved in its own file. The names of the files are printed.
########

import argparse
import csv
import os
from datetime import datetime
from Bio import Entrez

# Set up Entrez email as required by NCBI API
Entrez.email = "stavopro16@gmail.com"  # Replace with your email

def search_ncbi(database, term, max_results):
    """Search NCBI database and return search results."""
    handle = Entrez.esearch(db=database, term=term, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record

def fetch_ncbi_data(database, ids):
    """Fetch data for the given IDs from NCBI database."""
    handle = Entrez.efetch(db=database, id=','.join(ids), rettype="fasta", retmode="text")
    data = handle.read()
    handle.close()
    return data

def save_metadata(metadata_file, date, database, term, max_results, total_results):
    """Append metadata to the CSV file."""
    file_exists = os.path.isfile(metadata_file)
    with open(metadata_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["date", "database", "term", "max", "total"])
        writer.writerow([date, database, term, max_results, total_results])

def main():
    parser = argparse.ArgumentParser(description="Download data from NCBI.")
    parser.add_argument("--database", type=str, default="nucleotide", help="NCBI database to search (default: nucleotide)")
    parser.add_argument("--term", type=str, required=True, help="Search term")
    parser.add_argument("--number", type=int, default=10, help="Number of items to download (default: 10)")
    args = parser.parse_args()

    # Search NCBI
    search_results = search_ncbi(args.database, args.term, args.number)
    ids = search_results.get("IdList", [])
    total_results = int(search_results.get("Count", 0))

    # Fetch and save each record
    os.makedirs("downloads", exist_ok=True)
    filenames = []
    for i, ncbi_id in enumerate(ids):
        data = fetch_ncbi_data(args.database, [ncbi_id])
        filename = f"downloads/{args.term}_{i+1}.txt"
        with open(filename, "w") as file:
            file.write(data)
        filenames.append(filename)

    # Print filenames
    print("Downloaded files:")
    for filename in filenames:
        print(filename)

    # Save metadata
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_metadata("metadata.csv", date, args.database, args.term, args.number, total_results)

if __name__ == "__main__":
    main()
