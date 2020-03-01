# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


#Scriptname & version: Cardboy0's shapekey- and animation-compliant softbodies - V.1.0 
#Author: Cardboy0 (https://www.deviantart.com/cardboy0)
#Made for Blender 2.81a

######About this script:########
#   (for a more detailed explanation visit deviantart.com/cardboy0/art/Shapekey-animation-compliant-softbody-script-V1-0-826966931)
#The purpose of this script is to stop softbodies in Blender 2.81 from deforming without any collision by themselves, mainly when being animated. If you don't know what I mean,
#go into Blender, add a plane, scale it x2 in edit mode and subdivide it like 12 times (10 times and then 2 times again), then give it the following keyframed rotations: At frame 1 - X=90° Y=0° Z=0°, at frame 20 - X=270° Y=0° Z=45°. Then give it the softbody modifier, enable "goal" and "edges" (default values should be enough) in its properties and set its mass to 0kg (so it won't "wobble" because of gravity). 
#What you'd expect after baking is that nothing happens, because after all, there are no collision objects yet and the enabled goal should make it animate like the keyframes tell it to. What you'll see however, is that the plane gets deformed at some points, showing for instance some weird folding, maybe not to the extreme, but you can see it. The result is also a bit random, as you can bake it again and it will deform slightly different. So if you don't see it, bake it again. (For some reason that self-deforming-effect disappears if you already have a collision object in the scene, but it didn't disappear in my files with more complex meshes.)
#How I understand it now after dealing a little bit of time with it is that the goal and edges properties are in conflict with each other, both can deform the object. Somewhere in the official documentation it is written that they both influence the softbody, and you know, that makes sense. You want that, otherwise you could have no static objects slightly being deformed in midair or whatever.
#But the crucial part, which I think isn't mentioned enough in the documentation, is what the properties see as their goals. The "goal" property tries to animate it like its default animation, like the rotation of our plane or keyframed shapekeys, etc.
#The "edges" property however doesnt look at those animations. It tries to keep the softbody in its original shape, and thus fucks up the animation. If you animate with shapekeys, it will try to make the object go back to the shape of the Basis shapekey, if you're animating it in object mode it's probably the first keyframe of it. It sees any animations of those original shapes as exterior forces, and acts according to it.
#
#But in my case I didn't want that to happen, I wanted my softbody to keep its shape when being animated, but still be deformed by collision objects. So I made this script.
#It does what you originally expected the softbody properties to do, through shapekeys it will treat the shape of the object in frame x as the basis for that bake of frame x,
#meaning that the basis shapekeys will change to show the actual default animation, and thus not be deformed without collision. You don't have to worry if you're not using shapekeys,
#through the use of the 'NewTek MDD format' you can convert your animations into shapekeys that will play for each frame.
#Each frame will be baked individually, using the finished bake of the previous frame as the starting shape (as a shapekey), and the current shape of your object for that frame as the Basis shapekey.
#To create those Basis shapekeys you need to have 'Corrective Shape Keys' (mentioned again below) installed, it allows you to duplicate an object with shapekeys, removing all shapekeys and using the previous shapekey-mix as it's default shape now.
#Since only using one frame for baking each time appeared to not be enough to get decent results, I enabled this script to stretch your animation time. That way, it will have more frames between each original frame to bake them, slowing down the calculation but giving better results.
#Even if it bakes more than one frame, it will still only export the last baked frame through the .mdd format again and import that shape as a shapekey to another version of your original model without shapekeys, so in the end all the keyframed, individually imported shapekeys will together show the final, baked animation.
#It also stretches the time back to its default value afterwards.
#Since I had no prior experience in blender scripting, some operations where stolen from other people who found these to be solutions for certain problems I encountered, I left the links to those posts at the end of this script in the "reference"-paragraph.

#To see how the calculation is doing you should toggle the system console (in the window tab, Mac Users need to do it differently I think), after a frame has finished baking the script will say something like "Frame 34 done" since I wrote that somewhere in this script. That way you can be sure that the script is still working and your blender didnt just freeze.





### DRAWBACKS (at least the ones I know about):
# - Depending on your selected values the script will take a proportionally increased amount of time to finish compared to your original, "vanilla" softbody simulation. However it should only be a proportional correlation, meaning it might take 5, 10 or 15 times longer if you choose values like 5, 10 or 15, but not 5*1, 10*2, 15*3, or similar math stuff. It's still managable.
# - The script is only able to properly bake softbody sims that don't show any jiggle of the main animation mesh, or any other movent that's based on the use of velocity of vertices from the previous frames. Meaning you can bake for instance a collision-sphere colliding with a moving softbody-plane (making it dent), but if you try to let a softbody cube fall unto a collision plane, the cube will not show acceleration, meaning it falls with a constant velocity, and once it hits the plane it will likely only deform a tiny bit since there's almost no force from gravity, and it also won't jiggle in any way, because that requires the softbody sim to know the velocity of the vertices from previous frames, what this script prevents.
# - It might fuck up your scene, for instance it scales and later unscales all keyframes of all your objects, even unselected ones (it's not intended to do that, I just didn't find a different solution to that yet - although it also stretches your collision objects without you having to select them). So if something goes wrong, suddenly all your objects will have stretched keyframes. You should always make a backup of your blend file before you run this script.
# - The deformation it is intended to do might not work as well as you hoped it would, and you might have to increase some time-consuming values of this script to change that to the better, if it's possible at all. This script is far from perfect.
# - Your main animation mesh will show almost no self-induced deformation, but there'll still be some tiny amount of it that you might notice if you zoom in for instance. Basing on my understanding of the softbody system that shouldn't actually be the case, but apparentely I am wrong. Maybe it's fixable somehow.





### PLEASE READ: REQUIREMENTS

# - You need to have three Add-ons installed (they're already included in blender, you only have to enable them from the Add-ons tab in your preferences window):
#       "Animation: Corrective Shape Keys"
#       "Import-Export: NewTek MDD format"
#       "Interface: Copy Attributes Menu"

#       You only need to use the NewTek MDD format one yourself once, but the script needs all of them to work, since it uses some functions of those Add-ons.
# - Always backup your file before running this script, you don't want to get a nasty surprise.
# - Specify some values at the top of the script: desired beginning- and end-frame, as well as the "time stretch multiplier". I mentioned stretching your keyframes, and that's the value by which they'll get stretched. Only use integers.
# - You need to make 2 duplicates of your softbody object, and keep the original as a backup. The first duplicate (call it something like "main animation object", although the name doesnt matter to the script) needs to be exported as an .mdd, have all its modifiers applied (for deforming modifiers it probably won't really matter wether they're deleted or applied, but ones that change the amount of vertices, like a subdivision surface modifier, need to be applied), have all its shapekeys and keyframes deleted and then the previously exported .mmd imported on that same object again. That object should then show the exact same animation as before, only that it's now animated entirely through keyframes of shapekeys, one for each frame. The second duplicate (called "softbody dummy" from here on) should have no modifiers as well, except for a softbody modifier. The script will do many seperate softbody calculations on many seperate objects, and for each of those new objects it will use this duplicate to copy its softbody properties to those new objects. So, the softbody properties you give the softbody dummy are the ones this script will use. You could use a simple mesh with the same softbody properties as well, only that you then can't use vertex groups, for instance for the goal-property. Also you can technically give it other modifiers you want the new objects to get as well - like for instance a corrective smooth modifier - as all modifiers will be copied to the new objects. Sometimes it might fuck up the result though.
# - You need to only have those 2 duplicates selected when running the script, and the "main animation" one has to be the active object.
# - Depending on the framerate of your animation, you might want to change that value in the "bpy.ops.export_shape.mdd"-lines in this script, because I gave it a default value of 24 fps. I could simply do it via a single variable, but honestly I want to finally finish this script and don't want to do any further changes for now.




############ Important user-dependent values #############

baking_start_f = 1      #the desired first frame of your animation
baking_end_f   = 40     #the desired last frame of your animation

time_stretch_multiplier = 3        #stretches the timing of keyframes by that value, meaning with a value of 3 a keyframe at frame 1 will now be at frame 3, a keyframe at frame 2 now at frame 6, and so forth. This effectively means that the softbody calculations have more frames to work with. If you don't want to stretch anything just set it to 1.

#That's the only values you have to set yourself, the rest form here on is just the actual script.


############################################################################################################################################################################
############################################################################################################################################################################

import bpy
import os


print('script "Softbodies with animation/shapekeys calculation begin"')


############saving the (names of the) two selected objects###############
for i in bpy.context.selected_objects:
    if i == bpy.context.view_layer.objects.active:
        main_anim = i.name
    else:
        softbody_dummy = i.name        
print("main animation object: ", main_anim,', softbody dummy: ', softbody_dummy)
#########################################################################


############scaling the keyframes of the two selected objects############
old_type = bpy.context.area.type
bpy.context.area.type = 'DOPESHEET_EDITOR'
bpy.ops.action.select_all(action='SELECT')
bpy.context.scene.frame_set(0)
bpy.ops.transform.transform(mode='TIME_SCALE', value=(time_stretch_multiplier, 0, 0, 0), orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, -0, -0), (-0, -1, -0), (-0, -0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
#I'm gonna write it here again because it's rather important to know; the scaling-operation of keyframes somehow affects all selected keyframes of *all* objects - selected or unselected. To make sure there aren't any differences or objects left out, this script first selects all keyframes of all objects and then scales them.
bpy.ops.action.select_all(action='DESELECT')
bpy.context.area.type = old_type
#########################################################################


############creating the first import frame##############################
#This scipt uses the finished bake of the previous frame for the softbody sim of the current frame, but since we don't have a bake at the beginning we simply use the original shape at that frame, and for that it needs to be exported into an .mdd
bpy.context.scene.objects[softbody_dummy].select_set(False) #deselect the softbody dummy
blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
target_file = os.path.join(directory, 'single_frame_bakes.mdd')
bpy.ops.export_shape.mdd(filepath=target_file,frame_start=baking_start_f*time_stretch_multiplier, frame_end=baking_start_f*time_stretch_multiplier, fps=24.0, use_rest_frame=False)
#########################################################################


############creating the "permanent duplicate"###########################
#since we bake a softbody sim for each frame, we also need to give those finished bakes /shapes to an object on that frame to actually see it in the final animation. The "permanent duplicate" is that object, it gets more and more frames imported.
bpy.context.scene.frame_set(baking_start_f * time_stretch_multiplier)
bpy.ops.object.object_duplicate_flatten_modifiers()
main_anim_perm_dupl = bpy.context.selected_objects[0].name #(should be the only selected object if the script worked until now)
print("main animation permanent duplicate:",main_anim_perm_dupl)

bpy.context.view_layer.objects.active = bpy.context.scene.objects[main_anim_perm_dupl]
bpy.ops.import_shape.mdd(filepath=target_file, frame_start = (baking_start_f) *time_stretch_multiplier, frame_step=time_stretch_multiplier)
baking_start_f = baking_start_f + 1
#########################################################################


########################the big for-loop, repeats until every frame has been baked and put into keyframes.############
for x in range(baking_end_f - baking_start_f + 1):
    bpy.context.scene.frame_set(baking_start_f* time_stretch_multiplier)  #sets the current frame to one of the scaled keyframes of the main animation object
    print('current frame:',bpy.context.scene.frame_current)
    bpy.context.scene.objects[main_anim].select_set(True)
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[main_anim]
    ##print('ACTIVE OBJECT:',bpy.context.view_layer.objects.active)
    bpy.ops.object.object_duplicate_flatten_modifiers() #creating the keyframe-specific duplicate through the "corrective shapekeys" addon. The duplicate gets selected automatically when doing this
    main_anim_dupl = bpy.context.selected_objects[0].name #(should be the only selected object if the script worked until now)
    ##print("main animation temporary duplicate:",main_anim_dupl)
    bpy.ops.import_shape.mdd(filepath=target_file, frame_start=(baking_start_f - 1) * time_stretch_multiplier, frame_step = time_stretch_multiplier) #imports the "single_frames_bakes.mdd" on the duplicated object, with stretching of the keyframes according to the time stretch multiplier. This means that even when using no softbody modifier at all, it should still be back to its default shape at the last frame again, as the previous frame is only imported as a shapekey, whose value is keyframed to go down to 0 at the last frame.
    for o in (main_anim, main_anim_dupl):
        obj = bpy.context.scene.objects.get(o) 
        if obj: obj.select_set(True) 
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[main_anim]  
    bpy.ops.object.copy_obj_wei()                       #copying vertex weigths (through that 'Copy Attributes Menu' addon):
    bpy.ops.object.select_all(action='DESELECT')
    for o in (softbody_dummy, main_anim_dupl):
        obj = bpy.context.scene.objects.get(o)
        if obj: obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[softbody_dummy]
    bpy.ops.object.make_links_data(type='MODIFIERS')    #copying softbody modifier:
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects[main_anim_dupl]
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[main_anim_dupl]
    #change its softbody timerange of baking:
    bpy.context.object.modifiers["Softbody"].point_cache.frame_start = (baking_start_f-1) * time_stretch_multiplier
    bpy.context.object.modifiers["Softbody"].point_cache.frame_end = baking_start_f * time_stretch_multiplier
    #bake it:
    for modifier in bpy.context.scene.objects[main_anim_dupl].modifiers:
        if modifier.type == 'SOFT_BODY':
            override = {'scene': bpy.context.scene, 'active_object': bpy.context.scene.objects[main_anim_dupl], 'point_cache': modifier.point_cache}
            bpy.ops.ptcache.bake(override, bake=True)
            break
    #set the baked tempory duplicate as active again:
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[main_anim_dupl]
    #export the final baked frame into an .mdd and import it on the permanent duplicate:
    bpy.ops.export_shape.mdd(filepath=target_file,frame_start = baking_start_f * time_stretch_multiplier, frame_end = baking_start_f * time_stretch_multiplier, fps=24.0, use_rest_frame=False)
    bpy.context.view_layer.objects.active = bpy.context.scene.objects[main_anim_perm_dupl]
    bpy.ops.import_shape.mdd(filepath=target_file, frame_start = (baking_start_f) *time_stretch_multiplier, frame_step=time_stretch_multiplier)
    #delete the temporary duplicate again, a new one will be created in the next round of this for-loop.
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects[main_anim_dupl].select_set(True)
    bpy.ops.object.delete(use_global=False)
    print()
    print('Frame ',baking_start_f,' finished baking')
    print()
    baking_start_f = baking_start_f + 1
#########################################################################


############unstretching all keyframes###################################
old_type = bpy.context.area.type
bpy.context.area.type = 'DOPESHEET_EDITOR'
bpy.ops.action.select_all(action='SELECT')
bpy.context.scene.frame_set(0)
bpy.ops.transform.transform(mode='TIME_SCALE', value=(1/time_stretch_multiplier, 0, 0, 0), orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, -0, -0), (-0, -1, -0), (-0, -0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.action.select_all(action='DESELECT')
bpy.context.area.type = old_type

print()
print()
print('Script finished!')
print()
print()



#Used references (most of the problems that these are about aren't really something your average Joe, or me, could solve by himself):
#
#   - Ex-/importing .mdd :              https://blender.stackexchange.com/questions/84934/what-is-the-python-script-to-export-the-selected-meshes-in-obj
#   - Selecting certain objects:        https://blender.stackexchange.com/questions/132825/python-selecting-object-by-name-in-2-8
#   - Scaling keyframes:                https://blender.stackexchange.com/questions/14830/scale-keyframes-for-multiple-objects-with-a-script
#   - Baking a softbody via script:     https://blender.stackexchange.com/questions/6249/setting-the-context-for-cloth-bake
#   - Setting the current frame:        https://blender.stackexchange.com/questions/55637/what-is-the-python-script-to-set-the-current-frame

#   - Just a good tutorial about the basics of scripting in blender in general: https://www.youtube.com/watch?v=KNa5kJd2Epo ("Intro to Python Scripting in Blender - Workshop to automate tasks for artists")
