import glob
import argparse
import os
import re

parser = argparse.ArgumentParser(
    prog="renames all files with a given pattern",
    description="""renames all files with a given pattern""",
)

parser.add_argument(
    "-i", "--input", 
    default=".", 
    type=str, 
    dest="input", 
    help="Input path containing simulation data to render to png files.")

parser.add_argument(
    "--filename-pattern", 
    default="_*.png", 
    type=str, 
    dest="filename_pattern",
    help="the pattern of the filenames like '_*.png' ")

parser.add_argument(
    "--new-filename-pattern", 
    default="_*.png", 
    type=str, 
    dest="new_filename_pattern",
    help="the new pattern of the filenames like '_*.png' ")

parser.add_argument(
    "--zfill", 
    default=-1, 
    type=int, 
    dest="zfill",
    help="add zfill to the number in the filename, e.g. 3 for 001, 002, ...")

args = parser.parse_args()
print(args.input + args.filename_pattern)
filenamesList = glob.glob(args.input + args.filename_pattern)

fileTotal=len(filenamesList)
print("files found:"+ str(fileTotal))
for file in filenamesList:
    print(str(fileTotal) + " files left")
    fileTotal -= 1
    # Extract patterns before and after '*' in filename_pattern
    filename_pattern_parts = re.split(r'\*', args.filename_pattern)
    new_filename_pattern_parts = re.split(r'\*', args.new_filename_pattern)

    if len(filename_pattern_parts) != 2 or len(new_filename_pattern_parts) != 2:
        raise ValueError("Both filename_pattern and new_filename_pattern must contain exactly one '*'")

    before_star = filename_pattern_parts[0]
    after_star = filename_pattern_parts[1]
    new_before_star = new_filename_pattern_parts[0]
    new_after_star = new_filename_pattern_parts[1]

    starString = os.path.basename(file).replace(before_star, "").replace(after_star, "")
    print("starString: " + starString)
    if args.zfill > 0:
        starString = starString.zfill(args.zfill)
    new_file = f"{args.input}{new_before_star}{starString}{new_after_star}"
    os.rename(file, new_file)
    