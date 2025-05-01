from PIL import Image
import glob
import argparse

parser = argparse.ArgumentParser(
    prog="background white fill",
    description="""turn images from transparent to background white""",
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

args = parser.parse_args()
print(args.input + args.filename_pattern)
filenamesList = glob.glob(args.input + args.filename_pattern)

fileTotal=len(filenamesList)
for file in filenamesList:
    print(str(fileTotal) + " files left")
    fileTotal -= 1

    image = Image.open(file)
    new_image = Image.new("RGBA", image.size, "WHITE")
    new_image.paste(image, (0, 0), image) 
    newfile = file.replace(".png", "_white.png")
    # Save the new image with white background
    new_image.convert('RGB').save( newfile, "png")