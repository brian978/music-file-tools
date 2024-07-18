import csv
import os
import glob
import re
from unidecode import unidecode

csv_file_path = input("Enter the path to the CSV file to use for lookup: ")
target_folder = input("Enter the folder where to look for the files: ")

with open(csv_file_path, 'r') as f:
    reader = csv.DictReader(f, delimiter=';')  # Specify semicolon as delimiter
    songs = list(reader)

found_songs = []
not_found_songs = []


# Helper function to ignore case and special characters in filename
def normalize_string(s):
    s = unidecode(s).upper()  # replace non-ASCII characters with their closest equivalents and ignore case
    s = re.sub(r'\W+', '', s)  # ignore non-alphanumeric characters
    return s


for song in songs:
    artist = normalize_string(song["Artist"])
    title = normalize_string(song["Title"])

    # Get all files in target directory and subdirectories
    all_files = glob.glob(f'{target_folder}/**', recursive=True)

    for filename in all_files:
        basename = os.path.basename(filename)  # Get base name of file (without directory path)
        normalized_basename = normalize_string(basename)

        # Match normalized, uppercase versions of artist and title to basename
        if artist in normalized_basename and title in normalized_basename:
            found_songs.append(filename)
            break  # No need to look for more matches after a file has been found
    else:  # Only run if no break was encountered, i.e., no song was found
        not_found_songs.append(f"{song['Artist']} - {song['Title']}")

print("\nFound songs:")
found_songs = sorted(found_songs, key=lambda x: os.path.dirname(x))
found_songs = sorted(found_songs, key=lambda x: (os.path.dirname(x), os.path.basename(x).split(' - ')[0]))
for song in found_songs:
    print(song)

print("\nSongs not found:")
for song in not_found_songs:
    print(song)
