from render_usd import UsdRenderer
import igl
import os
from render_usd import UsdRenderer
from pxr import Usd
import argparse
from plyfile import PlyData, PlyElement
import numpy as np
from pxr import UsdGeom
import math

def list_of_strings(arg):
    return arg.split(',')

def read_ply(path):
    plydata = PlyData.read(path)
    vertex_count = plydata['vertex'].count
    V = np.zeros((vertex_count, 3))  # Initialize NumPy array for vertex positions
    V[:, 0] = plydata['vertex'].data['x']  # Fill x positions
    V[:, 1] = plydata['vertex'].data['y']  # Fill y positions
    V[:, 2] = plydata['vertex'].data['z']  # Fill z positions
    vertex_colors = np.zeros((vertex_count, 3))  # Initialize NumPy array for vertex colors
    vertex_colors[:, 0] = plydata['vertex'].data['red']   # Fill red channel
    vertex_colors[:, 1] = plydata['vertex'].data['green'] # Fill green channel
    vertex_colors[:, 2] = plydata['vertex'].data['blue']  # Fill blue channel
    vertex_colors /= 255.0  # Normalize RGB channels

    face_count = plydata['face'].count
    F = np.zeros((face_count, 3), dtype=int)  # Initialize NumPy array for face vertex IDs
    F[:, :] = np.vstack(plydata['face'].data['vertex_indices'])  # Fill face vertex IDs
    return V, F, vertex_colors

def export_obj_stop_motion_to_usd(renderer: UsdRenderer, folder: str, time_step: int, filename_patterns:list[str],extension:str, end_frame: int):
    import glob
    
    print("Setting up renderer for stop motion export")
    #automagically determine the zfiller and the number of frames
    zfiller = 0
    numFrames = 0
    for pattern in filename_patterns:
        filenamesList = glob.glob(folder+pattern+"*."+extension)
        for filename in filenamesList:
            try:
                # Extract the numeric part from the filename
                base_name = os.path.basename(filename).replace(pattern, "")
                number_part = ''.join(filter(str.isdigit, base_name))
                if number_part:
                    numFrames = max(numFrames, int(number_part))
                    # Find the zfill in filenames
                    if len(number_part) > zfiller:
                        zfiller = len(number_part)
            except ValueError:
                pass  # Ignore files that don't have numeric parts
    
    if end_frame > 0:
        numFrames = min(numFrames, end_frame)

    time = 0.0
    for frame in range(1,numFrames):
        time += time_step
        print("frame: ", frame,"/", numFrames, "time: ", time)
        renderer.begin_frame(time)
        for pattern in filename_patterns:
            # Check if the file exists
            if not os.path.exists(folder+pattern+str(frame).zfill(zfiller)+"."+extension):
                print("File does not exist: "+ folder+pattern+str(frame).zfill(zfiller)+"."+extension +" skipping this frame")
                continue # Skip this frame if the file does not exist

            # Read the mesh    
            vertex_colors_in = None
            if extension == "ply":
                V, F, vertex_colors_in = read_ply(folder+pattern+str(frame).zfill(zfiller)+"."+extension)
            else:
                V, F = igl.read_triangle_mesh(folder+pattern+str(frame).zfill(zfiller)+"."+extension)

            renderer.render_mesh(pattern, V, F, vertex_colors=vertex_colors_in, update_topology=True)
        renderer.end_frame()

parser = argparse.ArgumentParser(
    prog="obj 2 usd",
    description="""Creates animations in the USD file format.""",
)
parser.add_argument(
    "-i", "--input", 
    default=".", 
    type=str, 
    dest="input", 
    help="Input path containing simulation data to render to USD.")
parser.add_argument(
    "-o", "--output", 
    default="out.usd", 
    type=str, 
    dest="output",
    help="Output USD file (must end with .usd | .usda | .usdc)")
parser.add_argument(
    "--time-step", 
    default=1.0/60.0, 
    type=float, 
    dest="time_step", 
    help="time step size with which the simulation data input was generated. Default is 1/60.0 to match 60 fps.")
parser.add_argument(
    "--up-axis", 
    default="Z", 
    type=str, 
    dest="up_axis",
    help="The up axis, one of ('Y' or 'Z' or less probably 'X')")

parser.add_argument(
    "--filename-patterns", 
    default=["frame_001_"], 
    type=list_of_strings, 
    dest="filename_patterns",
    help="the pattern name of relevant entities in the filenames like 'frame_001', 'frame_002', etc. ")

parser.add_argument(
    "--file-type", 
    default="obj", 
    type=str, 
    dest="extension",
    help="file extension for the stop-motion")

parser.add_argument(
    "--end-frame", 
    default=-1, 
    type=int, 
    dest="end_frame",
    help="last frame to be exported")

parser.add_argument(
    "--meters-per-unit",
    default=1.0, 
    type=float, 
    dest="meters_per_unit",
    help="Meters per unit. Assumes 1 by default so it works with blender defaults.")

args = parser.parse_args()
stage = Usd.Stage.CreateNew(args.output)
renderer = UsdRenderer(stage, up_axis=args.up_axis, fps=math.floor(1.0/args.time_step), scaling=1.0)
UsdGeom.SetStageMetersPerUnit(renderer.stage, args.meters_per_unit)
export_obj_stop_motion_to_usd(renderer, args.input, args.time_step, args.filename_patterns,args.extension, args.end_frame)

renderer.save()
