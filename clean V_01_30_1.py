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


#Scriptname & version: Cardboy0's shapekey- and animation-compliant softbodies - V.1.26  (I often forget to actually update this number so don't trust it)
#Author: Cardboy0 (https://www.deviantart.com/cardboy0)
#Made for Blender 2.82



############user-dependent values #############

#####mandatory values:
baking_start_f = 1     #the desired first frame of your animation
baking_end_f   = 50  #the desired last frame of your animation

time_stretch_multiplier = 4
#Stretches the timing of keyframes by that value, meaning with a value of 3 a keyframe at frame 1 will now be at frame 3, a keyframe at frame 2 now at frame 6, and so forth. Beginning with Version 1.13 those extra frames will no longer be used to actually "stretch" the invidual animated frames, but only to be added to the end of each frame-bake, to give the softbody time to cool down any movement or jittering. If you don't want to stretch anything just set it to 1 (not recommended). It only improves the quality noticable up to a certain value (like 8, maybe a bit more, maybe a bit less), after which it will only further slow down the script - use values between 3 and 7.
######################


#####optional values:

desired_target_collection = "master_collection" 
#Name of the collection you want to have the results in (they also get their own collections). 'master_collection' is the default and refers to the collection of your current scene that all other collections of that scene are linked to.

main_anim_copy = False     
#When the baked results of this script are created, they won't have the original-animated frames of the unbaked timeframe on them, thus preventing you from using the script on them. This value creates a copy of your main-animation object, which also gets the last baked frame imported on it. This will allow you to continue the script at that frame using the new copy, as the first specified frame will be used without any baking involved, only as a reference for the next one. You don't *need* the script to do this, it's just a bit quicker than doing it yourself. To do it yourself: choose your original animation object and export all frames after your already baked frames as an mdd, then import it at that frame on the result of this script that was created previously (better use a duplicate for that). You basically just import the half the script didn't bake yet on the result yourself again, to get the rest of the original animation for the script on there again. Don't forget to make sure it still has its vertex groups, if not, you can copy them from the original animation object by pressing ctrl+c in the 3d-viewport.
anim_last_frame = 250   
#Only used if main_anim_copy = True. Tells the script up to which frame of the original anim it should import on the copy. If your scene ends at frame 1000 but you only animated the first 300 you want to set that value to 300, as the other 700 frames are useless and will just take up space and time.

max_baking_time = 0     
#in minutes (one second = 0.017 minutes) #Optional - if you give this variable a value higher than 0 the script will either stop once it has baked all frames, or until that amount of time in minutes has passed. It's useful for if you want the script to bake a lot of frames, but don't want to realise 2 hours later when you want to continue that it's only half finished, cause if you abort it yourself things will get messy. Set it to 120 minutes in that case and you can continue at the last baked frame later on by creating the previously mentioned main_anim_copy.

animate_vgroups = False 
#Requires the animall addon to work. If checked, your final result will have the vertex groups of your original object, but with keyframes that show how the vertex weights changed each frame. Is good for when you use VG-modifiers and want to see what they actually did during baking. However, I think that the copying of vertex weights will actually take some time depending on your vertex-count, not as long as the baking itself, but probably still like at least extra second per frame, so keep that in mind.

automatic_mdd = False
#If you don't want to do the preparing of your original object with mdd each time yourself (see requirements section), you can choose to let the script do it for you. If things don't work you'll have to do it yourself though. Also the softbody-dummy is still required, and he needs to have the applied shape of your orig-object. Main reason are vertex groups that you can only modify when mods like subdiv already have been applied. You can probably just use the "create duplicate for editing"-option in the shapekey-menu to create that "applied" copy for the softbody-dummy though.
#If True, the automatic copy will also not be deleted, but instead added to the final result collection, so you can use that from then on and disable this option or check if something went wrong.
#It will also do the same for your collision objects, and change the softbody-dummy's collision group to the one that has the new mdd versions in them. Meaning if you want to change that back, you have to change the collision collection yourself again. Same goes for vertex weight proximity modifiers that have one of the collision objects as a control object.
automatic_timerange = [90,130]
#only used if automatic_mdd is set to True, this will let you choose how many frames of your original object should be used when preparing. You may want to use more than your actual script-range is, since some things do things with later frames, e.g. the main_anim_copy. Default = [1,250]
######################

#Those are the only values you have to specify yourself.
#The remaining notes ('About this script') are maybe not really of interest to you, but you should definitely check out the requirements-section of that. Once you've done that, you've read all notes you need to read, and the remaining lines of this script are just code that's unimportant for you, meaning you can ignore them.

######About this script:########
#   (for other versions and a more detailed explanation visit https://www.deviantart.com/cardboy0/art/Cardboy0-s-SACS-Script-for-Blender-827936331) or https://github.com/Cardboy0/Cardboy0s-SACS/tree/master)
#   (for the "retroactive beautifier script", which I recommend using on the results of this script to make them look better using modifiers like corrective smooth with your original animation as the basis, visit https://www.deviantart.com/cardboy0/art/Retroactive-Beautifier-Script-832080660 or https://github.com/Cardboy0/retroactive-beautifier/tree/master)
#The purpose of this script is to stop softbodies in Blender 2.81 from deforming without any collision by themselves, mainly when being animated. If you don't know what I mean,
#go into Blender, add a plane, scale it x2 in edit mode and subdivide it like 12 times (10 times and then 2 times again), then give it the following keyframed rotations: At frame 1 - X=90° Y=0° Z=0°, at frame 20 - X=270° Y=0° Z=45°. Then give it the softbody modifier, enable "goal" and "edges" (default values should be enough) in its properties and set its mass to 0kg (so it won't "wobble" because of gravity). 
#What you'd expect after baking is that nothing happens, because after all, there are no collision objects yet and the enabled goal should make it animate like the keyframes tell it to. What you'll see however, is that the plane gets deformed at some points, showing for instance some weird folding, maybe not to the extreme, but you can see it. The result is also a bit random, as you can bake it again and it will deform slightly different. So if you don't see it, bake it again. (For some reason that self-deforming-effect disappears if you already have a collision object in the scene, but it didn't disappear in my files with more complex meshes.) This is just a simple plane, but if you, let's say, try to use an animated character as a softbody, everything gets way worse: your shapekeys won't work, everything that moves will show folds or wobble a bit like jelly, and other stuff; in other words: it will be impossible to ignore.
#How I understand it now after dealing a little bit of time with it is that the goal and edges properties are in conflict with each other, both can deform the object. Somewhere in the official documentation it is written that they both influence the softbody, and you know, that makes sense. You want that, otherwise you could have no static objects slightly being deformed in midair or whatever.
#But the crucial part, which I think isn't mentioned enough in the documentation, is what the properties see as their goals. The "goal" property tries to animate it like its default animation, like the rotation of our plane or keyframed shapekeys, etc.
#The "edges" property however doesnt look at those animations. It tries to keep the softbody in its original shape, and thus fucks up the animation. If you animate with shapekeys, it will try to make the object go back to the shape of the Basis shapekey, if you're animating it in object mode it's probably the first keyframe of it. It sees any animations of those original shapes as exterior forces, and acts according to it.
#
#But in my case I didn't want that to happen, I wanted my softbody to keep its shape when being animated, but still be deformed by collision objects. So I made this script.
#It does what you originally expected the softbody properties to do, through messing with shapekeys it will treat the shape of the object in frame x as the basis for that bake of frame x, meaning that the basis shapekeys will change to show the actual default animation, and thus not be deformed without collision. You don't have to worry if you're not using shapekeys, through the use of the 'NewTek MDD format' you can - and need to - convert your animations into shapekeys that will play for each frame.
#Each frame will be baked individually, using the finished bake of the previous frame as the starting shape (as a shapekey), and the current shape of your object for that frame as the Basis shapekey.
#To create those Basis shapekeys you need to have 'Corrective Shape Keys' (mentioned again below) installed, it allows you to duplicate an object with shapekeys, removing all shapekeys and using the previous shapekey-mix as it's default shape now.
#Since only using one frame for baking each time appeared to not be enough to get decent results, I enabled this script to add a specified number of frames for each bake to allow the softbody to calm down any movement. 
#Even if it bakes more than one frame, it will still only export the last baked frame through the .mdd format again and import that shape as a shapekey to another version of your original model without shapekeys, so in the end all the keyframed, individually imported shapekeys will together show the final, baked animation.
#It also stretches the time back to its default value afterwards.
#Since I had no prior experience in blender scripting, some operations where stolen from other people who found these to be solutions for certain problems I encountered, I left the links to those posts at the end of this script in the "reference"-paragraph.





### DRAWBACKS (at least the ones I know about):
# - Depending on your selected values the script will take a proportionally increased amount of time to finish compared to your original, "vanilla" softbody simulation. However it should only be a proportional correlation, meaning it might take 5, 10 or 15 times longer if you choose values like 5, 10 or 15, but not 5*1, 10*2, 15*3, or similar math stuff. It's still managable.
# - The script is only able to properly bake softbody sims that don't show any jiggle of the main animation mesh, or any other movent that's based on the use of velocity of vertices from the previous frames. Meaning you can bake for instance a collision-sphere colliding with a moving softbody-plane (making it dent), but if you try to let a softbody cube fall unto a collision plane, the cube will not show acceleration, meaning it falls with a constant velocity, and once it hits the plane it will likely only deform a tiny bit since there's almost no force from gravity, and it also won't jiggle in any way, because that requires the softbody sim to know the velocity of the vertices from previous frames, what this script prevents.
# - It might fuck up your scene, for instance it scales and later unscales all keyframes of all your objects, even unselected ones (it's not intended to do that, I just didn't find a different solution to that yet). So if something goes wrong, suddenly all your objects will have stretched keyframes. You should always make a backup of your blend file before you run this script. Also be aware that you can also undo this script running like any other action, which is probably way easier in most cases than reloading your backup.
# - The deformation it is intended to do might not work as well as you hoped it would, and you might have to increase some time-consuming values of this script to change that to the better, if it's possible at all. This script is far from perfect.
# - Your main animation mesh will show almost no self-induced deformation, but there'll still be some tiny amount of it that you might notice if you zoom in for instance. However you can decrease this "offset" by tweaking the goal damp value of your softbody, try values between 1 and 10.
# - You might notice that some vertices of your softbody will appear to "vibrate"/jitter when gliding against a collision object. Still need to find a fix for that.




### PLEASE READ: REQUIREMENTS

# - To see how the calculation is doing you should toggle the system console (in the window tab, Mac Users need to do it differently I think). It will show certain lines when stuff happens, like that a frame finished baking, how much time a frame needs on average, how much estimated time it will need to finish, etc.
# - You need to have three Add-ons installed (You only have to enable them from the Add-ons tab in your preferences window):
#       "Animation: Corrective Shape Keys"
#       "Import-Export: NewTek MDD format"
#       "Interface: Copy Attributes Menu"

#       All of them are needed for the script to work, but the NewTek MDD format is the most important one. It's also the addon you're going to have to use yourself to prepare your scene for this script.
# - Always backup your file before running this script, you don't want to get a nasty surprise.
# - Specify some values at the top of the script. Choose which frames you want to have baked, how much additional time you're ready to sacrifice for better results (time_stretch_multiplier), which collection you want the results to have in, wether you want a additional copy that makes for easier continuing of this script and what framerange that copy should have, the amount of time after which you want this script to end if it hasn't baked all frames yet, etc.
# - Preparing your scene: Only important if you don't use the automatic_mdd-option. Generally the rule of thumb is that you should always use the mdd-format for all the objects you want to have this script work with. If you export an object as an mdd and then reimport it, your object will animate exactly how it looked in the viewport when exporting, only that now it's being animated by shapekeys, one for each frame. But you need to know some things for this exporting/reimporting to work:
#    - The animation will only properly show if the object it's being imported on has the exact same amount of vertices, topology, etc. This means that, for instance if you had a subdivision modifier on your object active (in viewport) when exporting it, you need to apply this modifier before reimporting it, to get the same amount of vertices. All modifiers that are being shown in viewport when exporting should be applied afterwards, the hidden ones should be deleted. Also watch out for any mask-modifiers. This is the hard but probably almost always working way, an easier way is to go into the shapekey menu of your object and pressing "create duplicate for editing" in the shapekey specials section (the drop down arrow). It's an option from the "Corrective Shape Keys" addon and creates a static duplicate of your object with the same look, but no modifiers or shapekeys, basically everything that was seeable has been applied.
#    - Delete all keyframes before importing, since the importing will not delete anything by itself, meaning your animation will look weird since it's being played twice at the same time.
#    - Apply or clear all transformations of your object before importing.
#    - (Only for collision objects: the frame-range you're turning into shapekeys with the mdd-addon should be one frame more than the script frame-range. Otherwise the last frame will likely look weird.)
# - Further preparing: You need to have 3 types of objects for this script to work. The first one is your softbody, the one you want to see deformed. As already mentioned, make sure it's animated through shapekeys with the mdd-addon (and probably use a copy of the original for that). However, this one doesn't actually get any modifiers. The modifiers you want to see in the simulation, including the softbody modifier, need to be assigned to a duplicate of that first object. This one doesn't have to be animated, and you should also bake the softbody-modifier for like 1 frame yourself to make sure it's not getting rebaked by the script. You should call the first object something like "main_anim", the second one "softbody_dummy". Lastly, the collision objects: again, animated through mdd, and they need to be in specific collection which you can set as the collision collection in the softbody settings.
######Select both the softbody dummy and main_anim (this one has to be the active object), run this script, and wait for it to finish.





############################################################################################################################################################################
############################################################################################################################################################################

import bpy
import os
import time
import contextlib

print('##########################################################################')
print('script "Softbodies with animation/shapekeys calculation begin"')
print('##########################################################################')

C = bpy.context
D = bpy.data
O = bpy.ops

############some functions###############################################
#lets you select a list of objects (need to input the actual classes instead of their names), and also optionally choose the object you want to be active. By default it sets the first item in the list as active. The optional active object doesn't have to be in the list to be set as active, but then it still won't be selected.
#will deselect all other objects
#example: select_objects([Suzanne,Cube,Suzanne.001],Suzanne.004)
def select_objects(object_list, active_object = None):
    O.object.select_all(action='DESELECT')
    for i in object_list:
        i.select_set(True)
    if active_object == None:
        C.view_layer.objects.active = object_list[0]
    else:
        C.view_layer.objects.active = active_object


#applies the specified modifiers (use the actual names of the modifiers) of the specified object. The order in which the modifiers are applied is equal to their order in the list -> the first one gets applied first. It uses a context-override so it doesn't select/deselect any objects. Setting invert to True means that it will apply all modifiers of the object that are *not* in the given modifier list, however it will take the default mod-stack order. Choosing an empty list means it will apply all modifiers.
#example: apply_modifiers('Cube.001',["Wireframe.001","Subdivision"])
def apply_modifiers(object, modifier_list = [], invert = False):                    #had a problem with the context override, for future reference: if you want to do stuff with "active_object", you also have to change "object" to that object.
    override = C.copy()
    override['active_object'] = object
    override['object']= object
    if modifier_list == []:
        modifier_list = list(object.modifiers.keys())
    if invert == True:
        h_modifier_list = list(object.modifiers.keys())
        for i in modifier_list:
            if i in h_modifier_list:
                h_modifier_list.remove(i)
        modifier_list = h_modifier_list
    for i in modifier_list:
        if i in object.modifiers.keys():
            O.object.modifier_apply(override, apply_as='DATA', modifier = i)

            
#function that allows for hiding or unhiding certain, or all, modfiers. hide = False will unhide, an empty modifier list will do that with all mods. Often you don't want to hide the SB mod, so I made noSB to restrict it from being hidden. 
#example:  uhhh never used it lmao
def hide_mods(object = C.object, hide = True, modifier_list = [], noSB = True):
    if modifier_list == []:
        modifier_list = object.modifiers.keys()
    if noSB == True:
        for mods in mod_list:
            if mods in object.modifiers.keys(): 
                if object.modifiers[mods].type == 'SOFT_BODY':
                    mod_list.remove(mod)
                break
    for mods in modifier_list:
        if mods in object.modifiers.keys(): 
            if hide == False:
                object.modifiers[mods].show_viewport = True
            elif hide == True:
                object.modifiers[mods].show_viewport = False


#stretches time, if you want to unstretch it simply give it the value (1 / your_original_time_stretch_multiplier)
def stretch_time(l_time_stretch_multiplier):
    old_type = C.area.type
    C.area.type = 'DOPESHEET_EDITOR'
    O.action.select_all(action='SELECT')
    C.scene.frame_set(0)
    O.transform.transform(mode='TIME_SCALE', value=(l_time_stretch_multiplier, 0, 0, 0), orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, -0, -0), (-0, -1, -0), (-0, -0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    #I'm gonna write it here again because it's rather important to know; the scaling-operation of keyframes somehow affects all selected keyframes of *all* objects - selected or unselected. To make sure there aren't any differences or objects left out, this script first selects all keyframes of all objects and then scales them.
    O.action.select_all(action='DESELECT')
    C.area.type = old_type


#changes the min- and max-goal-value of the softbody to be 1 at the first frame of the bake, but resets them back to normal after that frame. Actually we will make the bake then start one frame earlier. That way the softbody looks exactly like it's shapekey at the "original" first frame (all vertices have a goal value of 1). If you don't do that the first frame of your bake will look like it's in that same shape as well, but you will get different results, I tried it. Apparently the first baked frame is treated a bit weird.    
def SB_keyframe_insert(start_frame, object): 
    C.scene.frame_set(start_frame + 1)
    object.soft_body.keyframe_insert(data_path = "goal_min")
    object.soft_body.keyframe_insert(data_path = "goal_max")
    C.scene.frame_set(start_frame)
    object.soft_body.goal_min = 1
    object.soft_body.goal_max = 1
    object.soft_body.keyframe_insert(data_path = "goal_min")
    object.soft_body.keyframe_insert(data_path = "goal_max")
    
    
#handles any input with predefined text and possible results.
#example: print(input_values_lines(2,'Change number of legs'))
def input_values_lines(default_value, line_text): #just the name
    while True:
        u_input = input(line_text+'\npress "s" to use default value \ncurrent default value:'+str(default_value)+"\n")
        if u_input == '':
            None
        elif u_input == 's':
            break
        else:
            default_value = u_input
            break
    return default_value


#checks if there already are any collections inside the target_collection that start with the collection_name (so it can detect i.e. myCollection.001 if you search for any myCollection). Returns the first found collection, or False if none were found.
#example: check_collections('Collec', bpy.context.scene.collection) #(bpy.context.scene.collection is the master-collection of your scene, it contains all other collections)
def check_collections (collection_name, target_collection): 
    if list(target_collection.children) == []:
        return False
    for i in target_collection.children:
        if i.name.startswith(collection_name):
            print(i)
            return i
    return(check_collections(collection_name, i))
#maybe it will lead to problems if the collection is also linked to other scenes/ collections, but I dont care about that for now.


#creates a collection with the collection_name inside the parent_collection. If you don't want duplicates to be created ("Collection.001" instead of "Collection" because there already is a "Collection") set avoid_duplicates as True. It will return the found duplicate - if there is one, otherwise it'll create a new one as normal.
#example: create_collection('third_Collection', parent_collection = bpy.data.collections['second_Collection'], avoid_duplicates = True)
def create_collection (collection_name, parent_collection = C.scene.collection, avoid_duplicates = False):
    if avoid_duplicates == False:
        new_collection = D.collections.new (name=collection_name)
        parent_collection.children.link(new_collection)
    elif avoid_duplicates == True:
        found_collection = check_collections(collection_name, parent_collection)
        print(found_collection)
        if found_collection == False:
            new_collection = D.collections.new (name=collection_name)
            parent_collection.children.link(new_collection)
        else:
            new_collection = found_collection
    return new_collection


#links and unlinks specified objects to the specified collections. To prevent bugs the objects should all share the same collections
#example: link_objects(bpy.context.selected_objects, bpy.context.scene.collection.children['New_Collection'], [bpy.context.scene.collection.children['Old_Collection']])
def link_objects(objects, link_to, unlink_to = []): #unlink_to needs to be a list (collections to unlink), None (unlink no collection), or not be specified at all (unlink all collections). link_to only uses one collection, so no list.
    if unlink_to == []:
        unlink_to = objects[0].users_collection    
    elif unlink_to == None:
        unlink_to = []
    
    for i in objects:
        for x in unlink_to:
            x.objects.unlink(i)
        link_to.objects.link(i)


#Creates duplicates of the chosen objects, that only have keyframes for the specified timespan. The last frame is also going to be the Basis-shapekey for the duplicate. Used for collision objects, if they aren't supposed to move anymore after a certain frame.
#example: print(duplicate_with_cut_keyframes(target_file_coll, bpy.context.selected_objects, [110,120], 1))
def duplicate_with_cut_keyframes(target_file, object_list, frames_export, l_frame_step = time_stretch_multiplier, mod_list = []): #frames_export like this: [4,10], last number is the basis shapekey.
    created_objects = []
    orig_frame = C.scene.frame_current
    C.scene.frame_set(frames_export[-1])
    for i in object_list:
        select_objects([i])
        O.export_shape.mdd (filepath=target_file, frame_start = frames_export[0], frame_end = frames_export[-1])
        O.object.object_duplicate_flatten_modifiers()
        new_object = C.selected_objects[0]
        created_objects = created_objects + [new_object]
        O.import_shape.mdd(filepath=target_file, frame_start=frames_export[0], frame_step = l_frame_step) 
        select_objects([i, new_object])
        O.object.copy_obj_wei()
        O.object.copy_obj_mod()    #Unlike the default modifier linking, this op (from the "copy attributes" addon) can copy collision modifiers as well. But I later found out that it resets all its values, meaning it's basically useless. I'm going to keep it in here anyways and copy each import-setting one by one.
        new_object.collision.damping = i.collision.damping
        new_object.collision.thickness_outer = i.collision.thickness_outer
        new_object.collision.thickness_inner = i.collision.thickness_inner
        new_object.collision.cloth_friction = i.collision.cloth_friction
        new_object.collision.use_culling = i.collision.use_culling
        new_object.collision.use_normal = i.collision.use_normal
    C.scene.frame_set(orig_frame)
    return created_objects
    

#Deletes the basis shapekey of the specified object, allowing the next shapekey in the stack to be the new basis. Notice that it will look like the new basis had a value of 1 before. If no object is specified, it will use the currently active object.    
def delete_basis_SK(s_object = None):
    if s_object != None:
        select_objects([s_object])
    orig_active_SK = C.object.active_shape_key_index
    C.object.active_shape_key_index = 0
    O.object.shape_key_remove(all=False)
    C.object.active_shape_key_index = orig_active_SK - 1
#########################################################################


with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):  #this prevents used functions printing statements in the system console by themselves, which are useless to the user and make it seem more chaotic.


    #####################Some stuff##########################################
    master_collection = C.scene.collection
    print_symbol_hash = '##########################################################################\n'
    print_symbol_asterik = '*****************************************************************\n'

    if desired_target_collection == 'master_collection':
        desired_target_collection = master_collection
    else: 
        desired_target_collection = D.collections[desired_target_collection]

    true_baking_start_f = baking_start_f
    default_frame = C.scene.frame_current

    time_script_begin = time.time()
    max_baking_time = max_baking_time * 60 #time gets measured in seconds and not minutes, but minutes is easier input for the user.
   
    if animate_vgroups == True:
        anima_props = bpy.data.window_managers["WinMan"].animall_properties

        #saving current values (Bool), this allows us to reset them back to their original state once this script is done. I don't like changing properties of the user without changing them back, that's annoying.
        checkboxes_animall_old = []
        checkboxes_animall_old += [anima_props.key_selected]
        checkboxes_animall_old += [anima_props.key_points]
        checkboxes_animall_old += [anima_props.key_ebevel]
        checkboxes_animall_old += [anima_props.key_crease]
        checkboxes_animall_old += [anima_props.key_vcols]
        checkboxes_animall_old += [anima_props.key_shape]
        checkboxes_animall_old += [anima_props.key_vbevel]
        checkboxes_animall_old += [anima_props.key_uvs]
        checkboxes_animall_old += [anima_props.key_vgroups]

        checkboxes_animall_new = [False, False,False,False,False, False,False,False,True] #these values will determine which checkbox of the anim_all is checked and thus what will be keyframes. In our case we just want the vgroups to be keyframed.
        #small note, since it led to some unneeded frustration on my side: Changing these values will not refresh how the checkboxes appear in the viewport, only once you hover your mouse over the panel will they refresh. I though the code just doesn't work and searched for too much time for another way to change them, until I realised that it did indeed work.
        anima_props.key_selected = checkboxes_animall_new[0]
        anima_props.key_points = checkboxes_animall_new[1]
        anima_props.key_ebevel = checkboxes_animall_new[2]
        anima_props.key_crease = checkboxes_animall_new[3]
        anima_props.key_vcols = checkboxes_animall_new[4]
        anima_props.key_shape = checkboxes_animall_new[5]
        anima_props.key_vbevel = checkboxes_animall_new[6]
        anima_props.key_uvs = checkboxes_animall_new[7]
        anima_props.key_vgroups = checkboxes_animall_new[8]
    #########################################################################


    ############assigning the two selected objects to variables, as well as the SB modifier##############

    for i in C.selected_objects:
        if i == C.view_layer.objects.active:
            main_anim = i                       #remember that if automatic_mdd == True, this is is the original and not the usable duplicate yet.
        else:
            softbody_dummy = i        

    for mods in softbody_dummy.modifiers:         
        if mods.type == 'SOFT_BODY':
            mod_SB = mods           #the softbody-modifier of the SB_dummy. Note however, that each time we create a new duplicate for baking, we must also assign its softbody modifier to a new variable since this one refers specifially to the SB_dummys SBmod. We could just work with it's name instead but that doesn't feel clean.
        break

    #also set their parent collection as the active one, otherwise problems might appear:
    C.view_layer.active_layer_collection = C.view_layer.layer_collection.children[softbody_dummy.users_collection[0].name]      #using the main_anim instead of softbody dummy here can lead to errors.
   
    
    ###now also the collision objects, put them into a new, temporary collection:
    #but first create the final collections:
    main_collection = create_collection('SACS_script_results', parent_collection = desired_target_collection, avoid_duplicates = True)
    sub_collection  = create_collection('frames'+str(true_baking_start_f)+'-'+str(baking_end_f), parent_collection = main_collection, avoid_duplicates = False)
    coll_orig_collision_objs = create_collection('orig collision objs', parent_collection = master_collection, avoid_duplicates = True)
    link_objects(mod_SB.settings.collision_collection.objects, coll_orig_collision_objs) #function unlinks them from all previous collections, meaning they're not inside the collision collection anymore
    #########################################################################
    
    ##setting up datapaths for the mdd-files that this script will create####
    blend_file_path = D.filepath
    directory = os.path.dirname(blend_file_path)
    target_file_calc = os.path.join(directory, 'single_frame_bakes_calc.mdd')
    target_file_col  = os.path.join(directory, 'temp collision objects')
    #########################################################################
    
    #################creating the automatic mdd copy#########################
if automatic_mdd == True:
    print('Creating mdd-versions of your original animated object, as well of the collision objects. This might take some seconds or minutes.\n\n')

with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):

    if automatic_mdd == True:
        select_objects([main_anim])
        O.export_shape.mdd (filepath = target_file_calc, frame_start = automatic_timerange[0], frame_end = automatic_timerange[1])
        O.object.object_duplicate_flatten_modifiers()
        main_anim = C.object            #now it's the actual new object, and not the original anymore
        O.import_shape.mdd(filepath=target_file_calc, frame_start=automatic_timerange[0], frame_step = 1)
        coll_temp_mdd_new = create_collection('temp mdd_collision objs', parent_collection = master_collection, avoid_duplicates = True)
        clone_list_coll = []     #this list has the purpose to know which new collision object came from which old one. That's so that the vertex weight proximity modifiers of the softbody-dummy can get that new object as their control object now. This doesn't matter normally, but here it does since things get weird if the control object gets hidden, which will likely be the case once the user decides to use the finished mdd-copies of the last script run and hide that other object instead. It will look like [[orig_coll1,mdd_coll1],[orig_coll,mdd_coll2],[orig_coll,mdd_coll3]]
        index = -1
        for i in coll_orig_collision_objs.objects:
            index += 1
            clone_list_coll += [[i]]
            select_objects([i])
            O.export_shape.mdd (filepath = target_file_calc, frame_start = automatic_timerange[0], frame_end = automatic_timerange[1]+1) #frame_end has one extra frame since the collision objects need to be animated at least one frame longer than the last baking frame is.
            O.object.object_duplicate_flatten_modifiers()
            C.object.name = 'mdd_'+i.name
            clone_list_coll[index] += [C.object]
            O.import_shape.mdd(filepath=target_file_calc, frame_start=automatic_timerange[0], frame_step = 1)
            link_objects([C.object], coll_temp_mdd_new)
            select_objects([i,clone_list_coll[index][1]])
            O.object.copy_obj_mod() #still needs the collision modifier of the original version.
        link_objects(coll_orig_collision_objs.objects, mod_SB.settings.collision_collection) #returns the original collision objects back to their original collection
        coll_orig_collision_objs = coll_temp_mdd_new
        coll_final_mdd_new = create_collection('mdd_collision objs', parent_collection = sub_collection, avoid_duplicates = False)
        mod_SB.settings.collision_collection = coll_final_mdd_new
        for i in softbody_dummy.modifiers:
            if i.type == 'VERTEX_WEIGHT_PROXIMITY':
                for y in clone_list_coll:
                    if y[0] == i.target:
                        i.target = y[1]
                    break
        
        
        
if automatic_mdd == True:
    print("mdd-versions created, they'll be in the a new collection which itself will be in the same collection as the final result.\nNote that the collision collection of your softbody properties will remain to be that new collection after the script is finished.\nDisable the automatic_mdd option and use the created mdd_versions of this script-run to skip this step on your next run.\nThe same goes for any Vertex Weight Proximity modifiers of your softbody-dummy, they'll now use the new mdd-version as their control object.")

with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):        

    #########################################################################
    
    
    ############scaling the keyframes of (almost?) ALL objects###############
    stretch_time(time_stretch_multiplier)
    #########################################################################


    ############creating the first import frame##############################
    #This scipt uses the finished bake of the previous frame for the softbody sim of the current frame, but since we don't have a bake at the beginning we simply use the original shape at that frame, and for that it needs to be exported into an .mdd
    select_objects([main_anim])
    O.export_shape.mdd (filepath = target_file_calc, frame_start = baking_start_f*time_stretch_multiplier, frame_end = baking_start_f*time_stretch_multiplier)
    #########################################################################


    ###creating the "permanent" duplicate that will show the final result#############
    #since we bake a softbody sim for each frame, we also need to give those finished bakes /shapes to an object on that frame to actually see it in the final animation. The "permanent duplicate" is that object, it gets more and more frames imported.
    C.scene.frame_set(baking_start_f * time_stretch_multiplier)
    O.object.object_duplicate_flatten_modifiers() #that's the function of the "Corrective Shape Keys" add-on that creates a static copy of your object.
    m_a_perm_dupl_calc = C.selected_objects[0]  #(should be the only selected object if the script worked until now)
    

    baking_start_f = baking_start_f + 1
    time_average = time.time()
    helper_start_f = true_baking_start_f
    time_5frame_average = time.time()
#print("time_average:",time_average)
#########################################################################

########################the big for-loop, repeats until every frame has been baked and put into keyframes.############
for x in range(baking_end_f - baking_start_f + 1):
    
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        temp_col_objects = duplicate_with_cut_keyframes(target_file_col, coll_orig_collision_objs.objects, [(baking_start_f) * time_stretch_multiplier, (baking_start_f) * time_stretch_multiplier + 1], 1, mod_list = [])
        link_objects(temp_col_objects, mod_SB.settings.collision_collection)
        
        
        C.scene.frame_set(baking_start_f* time_stretch_multiplier)  #sets the current frame to one of the scaled keyframes of the main animation object
        time_framebake = time.time()
        print("time_framebake:",time_framebake)
        
    print('\nCurrent frame:', int((C.scene.frame_current / time_stretch_multiplier)))
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        select_objects([main_anim])
        O.object.object_duplicate_flatten_modifiers() #creating the (temporary) keyframe-specific duplicate through the "corrective shapekeys" addon. The duplicate gets selected automatically when doing this
        main_anim_dupl = C.selected_objects[0] #(should be the only selected object)
        O.import_shape.mdd(filepath=target_file_calc, frame_start=(baking_start_f - 1) * time_stretch_multiplier, frame_step = 1) #imports the "single_frames_bakes.mdd" on the duplicated object, with stretching of the keyframes according to the time stretch multiplier. This means that even when using no softbody modifier at all, it should still be back to its default shape at the last frame again, as the previous frame is only imported as a shapekey, whose value is keyframed to go down to 0 at the last frame.
        select_objects([softbody_dummy, main_anim_dupl])
        O.object.copy_obj_wei()                       #copying vertex weigths (through that 'Copy Attributes Menu' addon)
        O.object.make_links_data(type='MODIFIERS')    #copying modifiers
        
        for mods in main_anim_dupl.modifiers:         
            if mods.type == 'SOFT_BODY':
                mod_SB_t = mods                     #mod_SB (without _t) specifically refers to the SB mod of the original SB-dummy, meaning we have to assign the SB-mod of the temporary duplicate to another, temporary variable to be able to refer to it.
                break
        
        ######
        #the next part is for vertex group modifiers that the user might have on his softbody_dummy. Good example is a vertex weight proximity modifier - VWP. Because you can't put it before the SB-mod in the mod-stack you can't effectively use them together for instance. We solve that by simply applying the VWP at the beginning of a frame, so the SB-mod *has* to use the modified vertex group. It doesn't affect the original softbody_dummy in any way (if I didn't mess up), which may be needed in other cases, but that will have to be dealed with when it's needed.
        
        select_objects([main_anim_dupl])
        O.object.duplicate()
        vw_duplicate = C.object
        vw_duplicate.active_shape_key_index = 1 #just to be sure. VWP uses the currently selected shapekey with a value of 1 as its base and ignores all others.
        bpy.ops.object.modifier_remove(modifier=mod_SB.name) #dont want to have any possible baked frames here.
        delete_basis_SK(vw_duplicate)
        select_objects([softbody_dummy, vw_duplicate])
        O.object.copy_obj_wei()             #don't know why I do that but I feel like i have to do that.
        apply_modifiers(vw_duplicate) #we can apply all modifiers - including the VWP to change Vertex weights. The only purpose of this object is to copy its applied vertex groups to the actual baking duplicate.
        
        
            
        #select_objects([vw_duplicate, softbody_dummy]) #if using a VWP global influence of 1 the original VG gets overwritten completely each frame, so there's no need to give it back to the SB_dummy, we only need to give it to the baking temp. duplicate as this one actually has to use it. Yes, I know, a value of 1 isn't always going to be the case but that's it for now.
        select_objects([vw_duplicate,main_anim_dupl])
        O.object.copy_obj_wei()
        if animate_vgroups == True: #small part to copy and keyframe the new vertex weights to the final result. If the object already has vertex-groups with the same names, they'll just get replaced but keep their keyframes, which is exactly what we need.
            select_objects([vw_duplicate, m_a_perm_dupl_calc])
            bpy.ops.object.copy_obj_wei()
            select_objects([m_a_perm_dupl_calc])
            for i in range(len(list(C.object.vertex_groups))):
                C.object.vertex_groups.active_index = i
                bpy.ops.anim.insert_keyframe_animall()
        select_objects([vw_duplicate])
        O.object.delete(use_global=False)
        
        ####
        
        #change its softbody timerange of baking:
        select_objects([main_anim_dupl])
        SB_keyframe_insert(((baking_start_f-1) * time_stretch_multiplier), main_anim_dupl)
        mod_SB_t.point_cache.frame_start = (baking_start_f-1) * time_stretch_multiplier - 1  #as explained before, since we keyframe the goal value to be exactly 1 at the starting frame, we then actually start the bake one frame earlier, as it wouldn't have an effect otherwise.  
        mod_SB_t.point_cache.frame_end = baking_start_f * time_stretch_multiplier
        
  
        #bake it:    
        override = {'scene': C.scene, 'active_object': main_anim_dupl, 'point_cache': mod_SB_t.point_cache}
        O.ptcache.bake(override, bake=True)
           
        #set the baked tempory duplicate as active again:
        select_objects([main_anim_dupl])
      
        #export the final baked frame into an .mdd and import it on the permanent duplicate:
        O.export_shape.mdd (filepath = target_file_calc, frame_start = baking_start_f * time_stretch_multiplier, frame_end = baking_start_f * time_stretch_multiplier)
        select_objects([m_a_perm_dupl_calc])
        O.import_shape.mdd(filepath=target_file_calc, frame_start = (baking_start_f) *time_stretch_multiplier, frame_step=time_stretch_multiplier)
        
        #delete the temporary duplicate again, a new one will be created in the next round of this for-loop.
        select_objects([main_anim_dupl])
        O.object.delete(use_global=False)
        
        #delete temp collision objects
        for i in mod_SB.settings.collision_collection.objects:
            select_objects([i])
            O.object.delete(use_global=False)
        
    #do the remaining stuff    
    ##print('\nFrame ',baking_start_f,' finished baking\n')
    baking_start_f = baking_start_f + 1
    print('Frame needed %s seconds to finish baking.' % int((round(((time.time() - time_framebake)),0))))
    time_framebake_average = round(((time.time() - time_average)/(baking_start_f - true_baking_start_f - 1)),0) #in seconds
    print('Current average baking time per frame: %s seconds' % (time_framebake_average))
    if helper_start_f+2 == baking_start_f:                      #every 5 frames, and once at the beginning, the average time between those 5 frames will be used to estimate the remaining time.
        helper_start_f = helper_start_f + 5
        if baking_start_f - true_baking_start_f == 2:
            time_5framebake_average_print = round((time.time() - time_5frame_average),0) #in seconds
        else:
            time_5framebake_average_print = round(((time.time() - time_5frame_average)/5),0) #in seconds
        print('***Estimated remaining time: %s minutes' % round(((baking_end_f - baking_start_f+1)*time_5framebake_average_print/60),2))
        time_5frame_average = time.time()
    
    if (time.time()-time_script_begin) >= max_baking_time and not max_baking_time == 0:
        print('\n'+print_symbol_hash + 'Runtime has reached specified limit of ' + str(round((max_baking_time/60),2)) + 'minutes; finishing script early \nlast baked frame:', baking_start_f-1,   '\n'+print_symbol_hash )
        baking_end_f = baking_start_f - 1
        break
    if max_baking_time != 0:
        print('Script ends in either '+str(baking_end_f - baking_start_f)+' frames\nor '+str(round(((max_baking_time  - (time.time() - time_script_begin))/60),1))+'minutes')
    elif max_baking_time == 0:
        print('Script ends in '+str(baking_end_f - baking_start_f + 1)+' frames\n')
        
#########################################################################


############resetting and sorting stuff##################################
stretch_time (1/time_stretch_multiplier)

print('\nAlmost finished!')


with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
    if animate_vgroups == True:
        #changing those animal-all checkboxes back to their default states
        anima_props.key_selected = checkboxes_animall_old[0]
        anima_props.key_points = checkboxes_animall_old[1]
        anima_props.key_ebevel = checkboxes_animall_old[2]
        anima_props.key_crease = checkboxes_animall_old[3]
        anima_props.key_vcols = checkboxes_animall_old[4]
        anima_props.key_shape = checkboxes_animall_old[5]
        anima_props.key_vbevel = checkboxes_animall_old[6]
        anima_props.key_uvs = checkboxes_animall_old[7]
        anima_props.key_vgroups = checkboxes_animall_old[8]
    
    
    
    m_a_perm_dupl_calc.name = "calc"



    coll_link_list = [m_a_perm_dupl_calc]       #all objects inside this list will be linked to our new collection later. They'll also be unlinked from their current linked collection, which should only be one.
    if automatic_mdd == True:
        main_anim.name = 'mdd_orig'
        coll_link_list += [main_anim]

    if main_anim_copy == True:
        target_file_ma_copy = os.path.join(directory, 'main_anim_copy with baked frame')
        select_objects([main_anim])
        O.export_shape.mdd (filepath = target_file_ma_copy, frame_start = baking_end_f + 1, frame_end = anim_last_frame)
        O.object.object_duplicate_flatten_modifiers()
        main_anim_copy = C.selected_objects[0]
        main_anim_copy.name = main_anim.name + ' baked copy'
        O.import_shape.mdd(filepath=target_file_ma_copy, frame_start = baking_end_f + 1, frame_step=1) 
        select_objects([m_a_perm_dupl_calc])
        O.export_shape.mdd (filepath = target_file_ma_copy, frame_start = baking_end_f, frame_end = baking_end_f)
        select_objects([main_anim_copy])
        O.import_shape.mdd(filepath=target_file_ma_copy, frame_start = baking_end_f, frame_step=1) 
        coll_link_list = coll_link_list + [main_anim_copy]
        select_objects([main_anim, main_anim_copy])
        O.object.copy_obj_wei()



    link_objects(coll_link_list, sub_collection, [])


    #put the original collision objects into the collision collection again.
    link_objects(coll_orig_collision_objs.objects, mod_SB.settings.collision_collection)
    bpy.data.collections.remove(coll_orig_collision_objs)   #removes the temporary needed collection for the collision objects. Sidenote: removing a collection will unlink all collections inside from your current scene.

    C.scene.frame_set(default_frame)  #small note, just noticed that using this line will make your current active object not be active anymore.
    select_objects([m_a_perm_dupl_calc])

    time_script_end = time.time()
print('\n\nScript took %s minutes to finish.' % (round(((time_script_end - time_script_begin)/60),2)))
print('One frame needed %s seconds on average to finish baking.' % (round(((time.time() - time_average)/(baking_end_f-true_baking_start_f)),1)))


print('\n\n'+2*print_symbol_asterik+'\nScript finished!\n\n'+2*print_symbol_asterik+'\n\n\n\n\n\n')


#Used references (most of the problems that these are about aren't really something your average Joe, or me, could solve by himself):
#
#   - Ex-/importing .mdd :              https://blender.stackexchange.com/questions/84934/what-is-the-python-script-to-export-the-selected-meshes-in-obj
#   - Selecting certain objects:        https://blender.stackexchange.com/questions/132825/python-selecting-object-by-name-in-2-8
#   - Scaling keyframes:                https://blender.stackexchange.com/questions/14830/scale-keyframes-for-multiple-objects-with-a-script
#   - Baking a softbody via script:     https://blender.stackexchange.com/questions/6249/setting-the-context-for-cloth-bake
#   - Setting the current frame:        https://blender.stackexchange.com/questions/55637/what-is-the-python-script-to-set-the-current-frame
#   - Overriding context:               https://blender.stackexchange.com/questions/13986/how-to-join-objects-with-python
#   - keyframing of physics values:     https://blender.stackexchange.com/questions/2620/insert-properties-keyframe-for-multiple-objects#2621
#   - working with collections:         https://devtalk.blender.org/t/where-to-find-collection-index-for-moving-an-object/3289    together with https://code.blender.org/2017/09/view-layers-and-collections/
#   - disable printing:                 https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python

#   - Just a good tutorial about the basics of scripting in blender in general: https://www.youtube.com/watch?v=KNa5kJd2Epo ("Intro to Python Scripting in Blender - Workshop to automate tasks for artists")





#small troubleshooting:
#   - If your softbody seems to get stuck, or even sucked into your collision object (CO), try inverting the normals of the CO. It happened to me in one of my files for all collision objects (I have no idea how), but that fixed it.
#   - If the script seems to run very slow even when only baking frames where there aren't any collisions yet, stop the script by pressing ctrl+c in the console, and undo the run-script-action. Just click around in your scene a bit, unhide your collision objects and select your 2 objects again. It sometimes happens to me, I don't really know why, but it almost always seems to not happen more than once in a row. If you actually let the script run until it's finished you'll notice that the results already start deforming too early (and probably not in the right way), for whatever reason.  
#   - visit https://www.deviantart.com/cardboy0/journal/Troubleshooting-823914200 for more troubleshooting

