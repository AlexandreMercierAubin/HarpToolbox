Harp Animation & Rendering Python Toolbox contains scripts to smooth out the process of exporting the outputs of simulators to rendering softwares.

# stopmotion2usd 
Converts sequences of models to a Universal Scene Description (USD).

install requirements
```
pip install -r .\requirements.txt
```

Arguments
* --input : Input path containing simulation data to render to USD
* -o : Output USD file (must end with .usd | .usda | .usdc)
* --time-step : Time step size between stop motion files with which the simulation data input was generated.
* --up-axis : The up axis, one of ('Y' or 'Z' or less probably 'X')
* --filename-patterns : The pattern name of relevant entities in the filenames like 'object_001_', 'object_002_', etc.
* --file-type : File extension for the stop-motion. Tested only with obj and ply. For ply vertex colors are exported.
* --end-frame : Optional last frame to be exported
* --meters-per-units : Number of meters per scene units. Sets default to 1 so blender does not shrink everything.

sample command:
```
python ./stopmotion2usd.py -i path/to/obj/sequence -o outputSequence.usd --time-step 0.01 --up-axis Z --filename-patterns frame_001_,frame_002_,frame_potat_
```

# background_white_fill
After rendering in blender, it is often wise to replace transparency with white pixels.
The background_white_fill python script does just that without having to rerender the scenes.

sample command
```
python ./background_white_fill.py -i path/to/png/sequence --filename-pattern _*.png
```
