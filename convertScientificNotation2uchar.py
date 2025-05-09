from PIL import Image
import glob
import argparse
import re
import os

parser = argparse.ArgumentParser(
    prog="changes the colors of the image from float to uchar",
    description="""changes the colors of the image from float to uchar""",
)

parser.add_argument(
    "-i", "--input", 
    default=".", 
    type=str, 
    dest="input", 
    help="Input path containing simulation data to render to png files.")

parser.add_argument(
    "--filename-pattern", 
    default="_*.ply", 
    type=str, 
    dest="filename_pattern",
    help="the pattern of the filenames like '_*.ply' ")

args = parser.parse_args()
print(args.input + args.filename_pattern)
filenamesList = glob.glob(args.input + args.filename_pattern)

fileTotal=len(filenamesList)
for file in filenamesList:
    print(str(fileTotal) + " files left")
    fileTotal -= 1

    # Read the entire file, process it, and write it back
    with open(file, 'r') as infile:
        content = infile.read()
    
    # Replace scientific notation numbers with their uchar equivalents
    processed_content = re.sub(
        r"[-+]?\d*\.\d+e[-+]?\d+",  # Regex to match scientific notation
        lambda match: str(int(float(match.group(0)) * 255)),  # Convert to uchar
        content
    )
    
    with open(file, 'w') as outfile:
        outfile.write(processed_content)