import glob
import argparse
import os
import re
import uuid

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

parser.add_argument(
    "--renumber",
    action="store_true",
    dest="renumber",
    help=(
        "replace the trailing digits at the end of the '*' part with sequential numbers "
        "(start, start+1, ...), instead of keeping the original digits"
    ),
)

parser.add_argument(
    "--renumber-start",
    default=1,
    type=int,
    dest="renumber_start",
    help="starting index used with --renumber (default: 1)",
)

args = parser.parse_args()

input_path = args.input
if input_path != "" and not input_path.endswith(("/", "\\")):
    input_path += os.sep

print(input_path + args.filename_pattern)
filenamesList = glob.glob(input_path + args.filename_pattern)

if args.renumber_start < 0:
    raise ValueError("--renumber-start must be >= 0")

fileTotal = len(filenamesList)
print("files found:" + str(fileTotal))

# Extract patterns before and after '*' in filename_pattern
filename_pattern_parts = re.split(r'\*', args.filename_pattern)
new_filename_pattern_parts = re.split(r'\*', args.new_filename_pattern)

if len(filename_pattern_parts) != 2 or len(new_filename_pattern_parts) != 2:
    raise ValueError("Both filename_pattern and new_filename_pattern must contain exactly one '*'")

before_star = filename_pattern_parts[0]
after_star = filename_pattern_parts[1]
new_before_star = new_filename_pattern_parts[0]
new_after_star = new_filename_pattern_parts[1]

# Sort files in numeric order based on the original trailing digits in the '*' part
# (avoids ASCII ordering like 1, 10, 2).
def _numeric_star_sort_key(path: str):
    basename = os.path.basename(path)
    star = basename.replace(before_star, "").replace(after_star, "")
    m = re.match(r"^(.*?)(\d+)$", star)
    if not m:
        return (star, float("inf"), basename)
    prefix = m.group(1)
    num = int(m.group(2))
    return (prefix, num, basename)

filenamesList = sorted(filenamesList, key=_numeric_star_sort_key)

rename_pairs = []

for idx, file in enumerate(filenamesList):
    print(str(fileTotal) + " files left")
    fileTotal -= 1

    basename = os.path.basename(file)
    starString = basename.replace(before_star, "").replace(after_star, "")
    print("starString: " + starString)

    if args.renumber:
        m = re.match(r"^(.*?)(\d+)$", starString)
        prefix = ""
        digits_width = 0
        if m:
            prefix = m.group(1)
            digits_width = len(m.group(2))

        seq_num = args.renumber_start + idx
        if args.zfill > 0:
            width = args.zfill
        else:
            width = digits_width

        if width > 0:
            starString = f"{prefix}{str(seq_num).zfill(width)}"
        else:
            starString = f"{prefix}{seq_num}"
    else:
        if args.zfill > 0:
            starString = starString.zfill(args.zfill)

    new_file = f"{input_path}{new_before_star}{starString}{new_after_star}"
    rename_pairs.append((file, new_file))

# Validate destination uniqueness
dests = [dst for _, dst in rename_pairs]
if len(dests) != len(set(dests)):
    raise ValueError("Renaming would create duplicate destination filenames.")

# Two-pass rename to avoid collisions (Windows rename fails if dest exists)
tmp_pairs = []
token = uuid.uuid4().hex
for src, _ in rename_pairs:
    tmp = src + f".tmp_renamePattern_{token}"
    if os.path.exists(tmp):
        raise FileExistsError(f"Temporary file already exists: {tmp}")
    os.rename(src, tmp)
    tmp_pairs.append(tmp)

for tmp, (_, dst) in zip(tmp_pairs, rename_pairs):
    os.rename(tmp, dst)
    