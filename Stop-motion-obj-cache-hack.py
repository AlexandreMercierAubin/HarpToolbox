#Nice code found from the issue section of the Stop-motion-obj addon for blender
#Makes life better.... way better!
#This bypasses the caching issues of the render animation button in that plugin by loading the frames individually.

import bpy

# Constants
NUMBER_OF_FRAMES = bpy.context.scene.frame_end - bpy.context.scene.frame_start

# prefix for img
IMG_PREFIX = bpy.context.scene.render.filepath

for frame_idx in range(NUMBER_OF_FRAMES+1):
    print(" > Render frame %04d out of %04d" % (frame_idx+ 1, NUMBER_OF_FRAMES+1))
    # Set correct frame
    bpy.context.scene.frame_current = bpy.context.scene.frame_start + frame_idx
      
    # Set name of output
    bpy.context.scene.render.filepath = IMG_PREFIX + '_%04d' % bpy.context.scene.frame_current
                                   
    # Render
    bpy.ops.render.render(write_still=True)
    
# Get everything back to normal    
bpy.context.scene.render.filepath = IMG_PREFIX
