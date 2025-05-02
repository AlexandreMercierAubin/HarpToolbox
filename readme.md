Harp Animation & Rendering Python Toolbox contains scripts to smooth out the process of exporting the outputs of simulators to rendering softwares.

# stopmotion2usd 
Converts sequences of models to a Universal Scene Description (USD).

Arguments
* --input : Input path containing simulation data to render to USD
* -o : Output USD file (must end with .usd | .usda | .usdc)
* --fps : Frames per second with which the simulation data input was generated.
* --up-axis : The up axis, one of ('Y' or 'Z' or less probably 'X')
* --filename-patterns : the pattern name of relevant entities in the filenames like 'object_001_', 'object_002_', etc.
* --file-type : file extension for the stop-motion. Tested only with obj and ply. For ply vertex colors are exported.
* --zfill : frame id zero padding. For instance 3 would look like 000,001,002, etc.
* --end-frame : optional last frame to be exported
* --meters-per-units : number of meters per scene units. Sets default to 1 so blender does not shrink everything.

sample command:
```
python ./stopmotion2usd.py -i path/to/obj/sequence -o outputSequence.usd --fps 100 --up-axis Z --filename-patterns frame_001_,frame_002_,frame_potat_
```

# background_white_fill
After rendering in blender, it is often wise to replace transparency with white pixels.
The background_white_fill python script does just that without having to rerender the scenes.

sample command
```
python ./background_white_fill.py -i path/to/png/sequence --filename-pattern _*.png
```
