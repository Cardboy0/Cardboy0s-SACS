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


#Scriptname & version: Cardboy0's shapekey- and animation-compliant softbodies - V.1.53.2.1  (I often forget to actually update this number so don't trust it)
#Author: Cardboy0 (https://twitter.com/cardboy0)
#Made for Blender 2.91



############SETTINGS#############

first_frame = 1     #the desired first frame of your animation
last_frame  = 50    #the desired last frame of your animation





#####optional settings#####

time_stretch_multiplier = 4     #(default = 4)
#increasing this value gives you better results but takes more time, decreasing it does the opposite.

desired_target_collection = "master_collection"     #(default = "master_collection")
#The name of the collection you want to contain the SACS results. "master_collection" is the name of the default collection that contains all other collections - but you can't actually see its name in Blender, so don't be confused about the name.

max_baking_time = 0 #minutes        #(default = 0)   
#If you give this variable a value higher than 0, the script will either stop once it has finished the last_frame, or until this amount of time has passed. 
#Useful for if you don't know how long the script will take to finish, because aborting the script will mess up your scene / results. 

automatic_scaling = True            #(default = True)
#If this option is activated, the script will automatically scale your objects to the biggest size possible while it is running. The biggest size depends on the biggest thickness of your collision objects. I found out that softbodies give better results the bigger they are. If you think that it's responsible for bad results, turn this option off. 

easy_mode = True                    #(default = True)
#There are a bunch of things that need to be done or prepared so this script can work. When easy_mode is enabled, most of these things will be done automatically by the script. Only disable it if you actually know how to prepare / do the stuff yourself.



#################################
###########DESCRIPTION###########

#For a way more detailed description or guide on how to use, visit the online manual: https://docs.google.com/document/d/1rpJIQqvXcGL9UN-JYzqRKVHk8xaMxgCKM0UYLyqDW_A/edit
#It contains explanations, helpful tutorials, examples, pictures, gifs and more. I highly recommend reading at least the Quickstart section of it (not added yet :(  ).

#You can download the newest version of this scipt at https://github.com/Cardboy0/Cardboy0s-SACS , and older versions at https://github.com/Cardboy0/Cardboy0s-SACS/tree/older-versions .


#This is a script that's supposed to help artists create belly-bulge fetish pornography in Blender. It's based on the softbody-simulation system of Blender. You can technically use it for your sfw needs as well, but I'm going to focus on the nsfw people here.
#It treats the belly of your model as a softbody plane, and you can use a collision object to deform it (Blender calculates the bulge result for us). For starters you can use an Ico-Sphere as a collision object, but you can also use animated models - for example big  W I E N E R S. Because they can have many vertices, that will require additional preparation however - described in the online manual. More vertices of your objects means more time the script will need to finish.

#It's not guaranteed to give good results, for example your result can show a certain jittering, or the bulge will not look smooth enough. Both of these 2 particular problems can be solved partially by using my "Retroactive-Beautifier" script (https://github.com/Cardboy0/retroactive-beautifier) , but it can't solve all problems that might appear.
#It can take A LOT OF TIME to finish, just one frame can take like 30 seconds.
#Also, the result will be a copy of your original object - without any modifiers and only animated through shapekeys.


#################################
########QUICK-START GUIDE########

#1. Create a new project in Blender
#2. In your preferences, enable the following 3 Add-ons:
#       "Corrective Shape Keys"
#       "NewTek MDD format"
#       "Copy Attributes Menu"
#   (Just type their names into the searchbar and check the box)
#3. Append your desired human model, and animate it. Try to only do a short animation for the first time to see if everything works, since the script can take a long time to finish.
#4. Give the model a new vertex group (call it something like "belly").
#       In edit mode, select the vertices of your models belly and assign them with a weight of 0.7 to the vertex group. Don't assign any other vertices.
#5. Add an Ico Sphere to your scene, and animate it to move through the belly. This is the object that will make the belly bulge, the "collision object".
#6. Give it a Collision modifier.
#       Tweak the Outer and Inner Thickness values. A value of 0.02 Outer Thickness means that the belly will start to deform once the Ico Sphere comes into a range of 2 cm. The outer Thickness points outwards of your object, the inner thickness points inwards. If your belly gets sucked inside the Ico Sphere when the SACS script has finished, you need to decrease the Inner Thickness.
#7. Create a new Collection. Name it "collision obs". Put the Ico Sphere inside that collection, and no other objects.
#8. Give your human model a Softbody modifier, and hide it. Its position in the modifier stack doesn't matter.
#       Try to hide any Subdivision Surface modifiers as well - the more vertices, the longer the script will take. You can still use it on the result again.
#9. In the softbody properties, set the following values (everything else can be left at default values):
#       Collision Collection: "collision obs"
#       Object  -> Mass = 0 kg
#       Goal    : enabled
#               -> Vertex Group: "belly"
#               -> Settings     -> Damping = 5
#       Edges   : enabled
#               -> Pull = 0.9
#               -> Damp = 13
#               -> Collision Face: enabled
#       Solver  -> Step Size Max = 900
#10. Head over to the "Scripting" Workspace inside your Blender project.
#11. In the text editor that's in the middle, open this script.
#12. Inside the script at the top there's a settings section. Change first_frame to the first frame of your animation, and last_frame to the last one.
#13. Below that are optional settings. Ignore them, but make sure that easy_mode = True .
#14. Select your Human model.
#15. Toggle the System Console in the "Window"-settings of your Blender file. This new window will display the progress of the script.
#16. Save your file in a new folder.
#17. In the text editor at the top right, press the "Run Script" button.
#18. Check the progress in the console window, and wait for it to finish.

#If you get an error, make sure that you undo the "Run Script" action in your Undo History. Otherwise things will get messy.




#################################
#############CHANGELOG###########

#V 1.53.2.1
#       - Extremely minor changes so it should now work with Blender 2.91
#V 1.53.2
#       - Fixed a bug were it didn't work when using a certain dick-object
#V 1.53
#       - Result works with Retroactive-Beautifier-Script again.
#V 1.50
#       - Completely rewrote the text at the beginning of the script.
#           + Added a Changelog
#       - Got rid of the need for a "SB_dummy". Now you only need to have one object selected when running this script, and it needs the animation AND the SB modifier.
#       - Added the easy_mode option to the optional settings, which is enabled by default. Does a lot of work the user would have to do themselves before.
#           + Does the import and export stuff with .mdd all by itself.
#           + Isolates the belly from the rest of the body while it runs, and fuses them back together once it has finished
#           + Adds the required "anchor row" of vertices to the goal vertex group itself, and sets the goal max and default values to 1 as well.
#       - removed the automatic_mdd option from the script.
#       - removed the "main_anim_copy" and "animate_vgroups" options from the settings. They've not been removed completely, I'm just like 80% sure that they won't give good results when combined with easy_mode right now, so I hid them.
#       - fixed a bug that gave you an error when the objects were in a subcollection of another collection.



#V 1.31 and earlier
#       - Some stuff lol. Didn't want to investigate everything for this again.





#################################
#######Boring Information########
########About the Script#########

#You don't have to read this, it's just for people who want to know more about why I made this script, how it grossly works, etc.

#"Why did you make this Script?". I like stomach bulge pornography. Was annoyed that there wasn't more good quality stuff on the internet. Decided to get into animating and creating quality stuff myself. Noticed that the only present ways to create stomach bulges were modelling, using premade shapekeys or other stuff that felt too hard or low-quality for me. Decided to use the softbody system of Blender to have the bulges correctly calculated for easy and decent quality results instead. Noticed that because of some reasons it can't just work like that. Created this script to make the softbody system work like that. Then also added other stuff that makes life easier for the user. 

#"What's the reason I need a Script instead of just using the default Softbody system?". If you use animated objects as a softbody, they will start to deform just *because* they are animated, even when there is no collision object. If you move a cube from one point to another with keyframes, the momentum will deform it. It only saves one "default" shape of your model. If your model would bend over, the belly would suddenly show folds like an accordion because the SB only remembers its default shape, the one where it is in rest position and her belly is stretched. If you make her belly bigger through shapekeys it will just instantly get flatter again, because the SB only remembers the Basis Shapekey. In short: Using the default SB system makes your animation look different from before. The script does a few things so it will keep looking like before while still using the SB-mod. At least if you use the right settings.

#"What's the basic mechanic?". I create temporary copies of the model with different properties and bake each frame individually, then copy the resulting shape to the final result model. The mdd-Format converts animation of an object, for instance through armature modifiers, corrective smooth, transformations etc. completely into shapekeys: The shape of the original object at frame 1 gets turned into a shapekey, and a new copy gets that shapekey keyframed at frame 1, then the next shapekey at frame 2, and so on. This is good, because the SB modifier treats the Basis shapekey of an object as its default shape, it tries to deform it back into that. So, through some exporting, importing and keyframing we start with the shapekey of the previous frame, and then disable it so only the Basis shapekey is active, WHICH, through another Add-on, will be the actual original shape of that object at this frame. If no collisions happened, the SB mod will just assume the Basis shape, which is the one the original animation has as well. If a collision does happen, it will deform. Then we can use the deformed shape as the starting shape of the next frame SB baking. If no collision happens, it will assume the Basis shape again, otherwise it will continue deforming. The script still needs to add some extra frames at the end of each bake (-> the "timestretch_multiplier" in the optional settings), because the SB mod needs a few frames to "calm down". This also means however, that your object will not save its momentum to the next frame, making stuff like jiggling or accelerating because of gravity impossible.


####
###Begin of the actual script:
####

############################################################################################################################################################################
############################################################################################################################################################################

import bpy
import os
import time
import contextlib
import sys
import bmesh
import random

print('##########################################################################')
print('script "Softbodies with animation/shapekeys calculation begin"')
print('##########################################################################')

main_anim_copy = False
anim_last_frame = 250 
animate_vgroups = False

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


#applies the specified modifiers (use the actual names of the modifiers) of the specified object. The order in which the modifiers are applied is equal to their order in the list -> the first one gets applied first. It uses a context-override so it doesn't select/deselect any objects. Setting invert to True means that it will apply all modifiers of the object that are *not* in the given modifier list, however it will take the default mod-stack order. Choosing an empty list means it will apply all modifiers. If delete_hidden is set to True, it will delete, instead of apply, a modifier if it is set to hidden.
#example: apply_modifiers('Cube.001',["Wireframe.001","Subdivision"])
def apply_modifiers(object, modifier_list = [], invert = False, delete_hidden = False):                    #had a problem with the context override, for future reference: if you want to do stuff with "active_object", you also have to change "object" to that object.
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
    if delete_hidden == True:
        for i in modifier_list:
            if i in object.modifiers.keys():
                if object.modifiers[i].show_viewport == True:
                    try:
                        O.object.modifier_apply(override, modifier = i)
                    except RuntimeError:
                        print("OOPS! MODIFIER", i, "IS DISABLED! IT WILL BE DELETED") #trying to apply a disabled modifiier leads to an error message, but I didn't figure out how to check if it's disabled. Thus, we'll have to deal with the error instead.
                        print("ERROR TYPE IS", sys.exc_info()[0])
                        O.object.modifier_remove(modifier = i)   
                elif object.modifiers[i].show_viewport == False:
                    O.object.modifier_remove(modifier = i)
    elif delete_hidden == False:
        for i in modifier_list:
            if i in object.modifiers.keys():
                O.object.modifier_apply(override, modifier = i)

            
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


#checks if there already are any collections inside the target_collection that start with the collection_name (so it can detect i.e. myCollection.001 if you search for any myCollection). Returns the first found collection, or False if none were found. Checks child collections of child collections as well, and so on.
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
    

#Recursivly transverse layer_collection for a particular name. For whatever reason, a viewlayer collection isn't an actual collection class, but another special one. Meaning, you can't work with collections here, and also lack some features that collections have.
#Shamelessy stolen from the user johnzero7 who posted the original definition in a StackExchange thread: https://blender.stackexchange.com/questions/127403/change-active-collection  
#example: find_viewlayer_collection('The name of your searched collection')
def find_viewlayer_collection(collName, layerColl = None):
    if layerColl == None:
        layerColl = C.view_layer.layer_collection #layerColl will be the master-collection of the scene by default
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = find_viewlayer_collection(collName, layer)
        if found:
            return found
            
            
###This function deals with vertex indices of objects, mainly resetting them to their original indices. You give your original object a cSK (Calibrating Shapekey) with the subfunction = "create_cSK". Then you make sure that the objects that base off of this original one keep that shapekey or get it transfered to from the original with "transfer_cSK". Once vertex indices are messed up, you may use "reset_vi" to reset them back to the indices of the original object. For that, the cSKs of both objects have to still look exactly the same, since the function compares vertex coordinates to assign indices. Delete a cSK after finishing with "delete_cSK". The cSKs need also to have the same name everytime as it is used for identification.
#Example: vertindex_calibrate("create_cSK", "cSK_123r5qwadasd", D.objects['Icosphere']) . A passive_object is only required for the subfunctions "transfer_cSK" and "reset_vi", and in both cases that should be the original object.
def vertindex_calibrate(subfunction, cSK_name, active_object, passive_object = None):
    
    def find_SK (Obj, SK_name):
        for i in Obj.data.shape_keys.key_blocks:
            if i.name == SK_name:
                SK = i
                break
        return SK
    
    
    O.object.mode_set(mode='OBJECT') #CHANGING THE COORDINATES DOESNT CHANGE ANYTHING WHEN IN EDIT MODE - maybe verts need to be "updated" somehow?
    Obj_active = active_object
    Obj_passive = passive_object
    if Obj_passive == None:
        Obj_passive = Obj_active    #some subfunctions dont require a second object
    
    soSK_act    = Obj_active.show_only_shape_key
    soSK_pass   = Obj_passive.show_only_shape_key
    ueSK_act    = Obj_active.use_shape_key_edit_mode
    ueSK_pass   = Obj_passive.use_shape_key_edit_mode
    SKact_orig  = Obj_active.active_shape_key
    SKpass_orig = Obj_passive.active_shape_key
    
    mods_unhidden_act = []
    mods_unhidden_pass = []
    for obj, mod_list in zip([Obj_active, Obj_passive],[mods_unhidden_act, mods_unhidden_pass]):
        for mod in obj.modifiers:
            if mod.show_viewport == True:
                mod_list = mod_list + [mod]
                mod.show_viewport == False
    
    O.object.select_all(action='DESELECT')
    Obj_active.select_set(True)
    Obj_passive.select_set(True)
    C.view_layer.objects.active = Obj_active
    
    
    
    if subfunction == "create_cSK":
        Obj_active.show_only_shape_key = True
        Obj_active.active_shape_key_index = 0
        O.object.object_duplicate_flatten_modifiers()
        Obj_static = C.object
        g = 1
        
        while True:
            if len(Obj_static.data.vertices) > g**3:
                g = g +1
            else:
                break
        cSK_COs = [[0,0,0]]
        for i in [0,1,2]:
            for e in cSK_COs:   #should not update while loop is running
                for c in range(g-1):
                    c = c + 1
                    temp_CO     = e.copy()
                    temp_CO[i]  = temp_CO[i] + c
                    cSK_COs     = cSK_COs + [temp_CO]
                    
        for i in range(len(Obj_static.data.vertices)):
            Obj_static.data.vertices[i].co = cSK_COs[i]
            
        O.object.select_all(action='DESELECT')
        Obj_active.select_set(True)
        Obj_static.select_set(True)
        C.view_layer.objects.active = Obj_active
        
        O.object.join_shapes()
        cSK_act = Obj_active.data.shape_keys.key_blocks[-1]
        cSK_act.name = cSK_name
        
        O.object.select_all(action='DESELECT')
        Obj_static.select_set(True)
        O.object.delete(use_global=False)



    elif subfunction == "transfer_cSK":
        cSK_pass = find_SK(Obj_passive, cSK_name)

        Obj_passive.active_shape_key_index = list(Obj_passive.data.shape_keys.key_blocks).index(cSK_pass)
        Obj_passive.show_only_shape_key = True
        
        O.object.join_shapes()
        
        cSK_act = Obj_active.data.shape_keys.key_blocks[-1]
        cSK_act.name = cSK_name



    elif subfunction == "reset_vi":
        cSK_act  = find_SK (Obj_active , cSK_name)
        cSK_pass = find_SK (Obj_passive, cSK_name)
        
        for obj, SK in zip([Obj_active, Obj_passive], [cSK_act, cSK_pass]):
            obj.active_shape_key_index = list(obj.data.shape_keys.key_blocks).index(SK) #using .active_shapekey instead doesn't work since it's read-only
            obj.use_shape_key_edit_mode = False

        O.object.mode_set(mode='EDIT')
        bm_Obj_passive = bmesh.from_edit_mesh(Obj_passive.data)
        bm_Obj_active = bmesh.from_edit_mesh(Obj_active.data)
        for i in bm_Obj_passive.verts:
            for e in bm_Obj_active.verts:
                if i.co == e.co:
                    e.index = i.index
                    break
        
        #these two lines are what makes the vertex indices actually change / update
        bm_Obj_active.verts.sort()
        bmesh.update_edit_mesh(Obj_active.data)
 
        O.object.mode_set(mode='OBJECT')
    
        cSK_act = "VI-RESET SUCCESSFUL"
    
    
    
    elif subfunction == "delete_cSK":
        cSK_act = find_SK (Obj_active, cSK_name)
        
        Obj_active.shape_key_remove(cSK_act)
        
        csK_act = "DELETION SUCCESSFUL"

    
    
    else:
        return("ERROR - INVALID SUBFUNCTION VALUE")



    Obj_active.show_only_shape_key      = soSK_act
    Obj_passive.show_only_shape_key     = soSK_pass
    Obj_active.use_shape_key_edit_mode  = ueSK_act
    Obj_passive.use_shape_key_edit_mode = ueSK_pass    
    for obj,SK in zip([Obj_active, Obj_passive],[SKact_orig, SKpass_orig]):
        if SK != None: #if the object had no SKs at the beginning, the SK-variable will be a None-object
            obj.active_shape_key_index = list(obj.data.shape_keys.key_blocks).index(SK)
        else:
            obj.active_shape_key_index = 0

    for mod_list in [mods_unhidden_act, mods_unhidden_pass]:
        for mod in mod_list:
            mod.show_viewport == True

    return cSK_act
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

    true_first_frame = first_frame
    true_last_frame   = last_frame
    default_frame = C.scene.frame_current
    ori_av_layercoll = C.view_layer.active_layer_collection #original active viewlayer collection - to reset it at the end of this script

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

if easy_mode == True: #does a lot of automation
    print('easy_mode = True    => Peparing your scene...')
    print('    ... doing some stuff')
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f): #mute all prints
        Obj_original = C.object
        O.object.duplicate()
        Obj_main = C.object

        blend_file_path = D.filepath #the lines are going to appear another time in this script, but it doesn't really matter if they're written twice.
        directory = os.path.dirname(blend_file_path)
        target_file_calc = os.path.join(directory, 'single_frame_bakes_calc.mdd')
        target_file_col  = os.path.join(directory, 'temp collision objects')

        for mods in Obj_main.modifiers:         
            if mods.type == 'SOFT_BODY':
                ModSB_main = mods
                break
        for mods in Obj_original.modifiers:         
            if mods.type == 'SOFT_BODY':
                ModSB_original = mods
                break
        
        show_viewport_of_SB_orig = ModSB_original.show_viewport #"saving" the original state of the SB mod
        ModSB_original.show_viewport = False #...unhidden just never gives anything but problems
        ModSB_main.show_viewport = False #Noticed that when it's unhidden, an error will appear later on when applying the modifiers which causes blender to crash completely
        
        O.object.mode_set_with_submode(mode='EDIT',  mesh_select_mode = {"VERT"} ) #me must make sure that only vertex selection is possible in edit mode, otherwise problems will appear
        O.object.mode_set(mode='OBJECT')

        Coll_mddcollision_objs = create_collection ("mdd_collision_objects", avoid_duplicates = False)
        select_objects(ModSB_main.settings.collision_collection.objects)
        O.object.duplicate() #skin modifier gives a different copy? Even manually? Skin is just weird, ignore for now.
        L_mddcollision_objs = C.selected_objects
        
        link_objects(L_mddcollision_objs, Coll_mddcollision_objs)
#########################################################################
    print('    ... Converting your objects with the .mdd Format')
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        #exporting and importing the .mdd files as well as applying/deleting modifiers and changing VGroups
        for i in [Obj_main]+L_mddcollision_objs:
            #exporting and applying mods                                                         
            select_objects([i])
            if i == Obj_main:    
                O.export_shape.mdd (filepath = target_file_calc, frame_start = first_frame, frame_end = last_frame)
                
                #before applying the modifiers, we will assign the SB-goal VG to a variable, since we need to edit it later. We will also create a copy of SB-goal, with the sole purpose of using it to "reset" the original SB-goal to its original weights once the Script has finished, using the vertex weight mix modifier. It could lead to problems for the user if vertex groups change when using the script.
                VG_goal_name    = ModSB_main.settings.vertex_group_goal #the mod itself only returns a string instead of the required VG-type
                VG_goal         = Obj_main.vertex_groups[VG_goal_name]
                Obj_main.vertex_groups.active_index = VG_goal.index
                O.object.vertex_group_copy() #when copying is finished, the new copy is active by default
                VG_goal_backup  = Obj_main.vertex_groups.active
                #setting armatures to rest position. We'll not do this for the collision objects since they will just be deleted later on. The only purpose of this is so that the bulge result has the rest position as its basis shapekey, it's not actually required.
                

                select_objects([i])
                armature_positions = [] #while we do use only a copy of the original model, we use the original rig. We'll set it to Rest position shortly after this line, but to make things not annoying we'll have to reset the positions to how they were before, and this list tells how they were. 
                for mods in i.modifiers:         
                    if mods.type == 'ARMATURE':
                        armature_positions = armature_positions + [mods.object.data.pose_position]
                        mods.object.data.pose_position = "REST"
     
            else:
                O.export_shape.mdd (filepath = target_file_calc, frame_start = first_frame, frame_end = last_frame + 1) #the collision objects need to be animated through shapekeys for one more additional frame, otherwise it's very likely to fuck things up
                 
            L_mods_collision = []
            apply_invert = False
            select_objects([i])
            i.shape_key_clear()     #modifiers can't be applied when the object has shapekeys
            for mods in i.modifiers:
                if mods.type == 'COLLISION':
                    apply_invert = True
                    L_mods_collision = L_mods_collision + [mods.name]
            apply_modifiers(object = i, modifier_list = L_mods_collision, invert = apply_invert, delete_hidden = True)            #applys/deletes all modifiers except any collision modifiers the object might have
            O.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            O.object.transform_apply(location=True, rotation=True, scale=True)
            i.animation_data_clear() #deletes all keyframes
            if i == Obj_main: #resetting the armatures of Obj_main to their original state (rest or pose) since we temporily changed them to rest.
                n = 0                     
                for mods in Obj_original.modifiers:         
                    if mods.type == 'ARMATURE':
                        mods.object.data.pose_position = armature_positions[n]
                        n = n + 1
            
            ###importing
            select_objects([i])
            O.import_shape.mdd(filepath=target_file_calc, frame_start = first_frame)
        
        n_cSK = "cSK_" + str(random.randint(1000000,9999999)) #using the same name for every run of this script could lead to problems, so we'll choose a random name for each run instead. 
        vertindex_calibrate("create_cSK", n_cSK, Obj_main)
        select_objects([Obj_main])
        O.object.duplicate()
        Obj_VI_main = C.selected_objects[0]
        Obj_VI_main.name = "VI_OBJECT"

    print('    ... Preparing the goal vertex group')
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        ###giving the SB_goal VG anchor vertices. "Anchor" because with the right values, these vertices will not deform in any way through the softbody sim. This is especially helpful since we isolate the belly from the body and want to fuse them back together once everything is finished, and since those anchor vertices will not change their animation, we can use them as perfect merging points. Also they will keep the belly from being pushed around in space. 
        VG_anchor = Obj_main.vertex_groups.new() #<-not actually used here yet, it's for dealing with fusing at the end.
        select_objects([Obj_main])
        Obj_main.vertex_groups.active_index = VG_goal.index
        O.object.mode_set(mode='EDIT')
        O.mesh.select_all(action='DESELECT')
        O.object.vertex_group_select()
        O.mesh.select_more()
        O.object.vertex_group_deselect()
        C.scene.tool_settings.vertex_group_weight = 1
        O.object.vertex_group_assign()
        Obj_main.vertex_groups.active = VG_anchor
        O.object.vertex_group_assign()
        O.object.mode_set(mode='OBJECT')

    print('    ... Isolating the belly from the body into its own object')
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        ###isolating            For reasons I dont fully understand, we can't just use the whole remaining body as anchor points. Because even though these anchor points will not deform in any way through the Softbody Sim, they will still influence the time it takes to bake, increasing it significantly. So, the best idea I came up with to prevent this issue, is to split the belly part into its own object, do the baking, and then at the end fuse it and the body back together again. However, with versions past 1.50, the isolating and fusing will be done a bit more complicated. Instead of just merging vertices with the same coordinates together later on, the script will remember each vertex and will only merge the same ones. This makes a difference when the original model already has vertices at the same coordinates, since those would've normally been merged together as well.
        vertex_indices      = []    #When fusing two objects back together later on, we need to know which vertex of one object is the same one in the other object. We'll use this method instead of their coordinates since some models can have multiple vertices at the same coordinates, and then we couldn't distinguish between those.
        vertex_VGs_belly    = []    #due to problems with calling vertices, each vertex will be assigned to a single Vertex Group, so that we can use those Vertex Groups to call the vertices. Maybe I should use the cSK_calibrate function here as well instead, but that's for another time.
        vertex_VGs_body     = []
        
        select_objects([Obj_main])
        O.object.mode_set(mode='EDIT') #bmesh stuff requires edit mode
        bm_Obj_main = bmesh.from_edit_mesh(Obj_main.data)      #code altered from a stackexchange post of user "nadal zkz" - link: https://blender.stackexchange.com/questions/49931/select-vertices-by-their-indices-by-vertex-id
        vertices = [e for e in bm_Obj_main.verts]
        O.mesh.select_all(action='DESELECT')
        Obj_main.vertex_groups.active = VG_anchor
        O.object.vertex_group_select()
        for i in vertices:
            if i.select == True:            #saves only the indices of vertices which are inside VG_anchor - and thus are required for fusing later on
                vertex_indices = vertex_indices + [i.index]
        O.object.mode_set(mode='OBJECT')

        for i in vertex_indices:
            VG_new = Obj_main.vertex_groups.new()
            VG_new.add([i], 1, 'ADD') #doesn't work in edit mode
            VG_new.name = 'vertex ' + str(i) #not necessary, just for programming comfort
            vertex_VGs_belly = vertex_VGs_belly + [VG_new] #creating a VG for each single vertex of VG_anchor, and then saving those VGs to a list.
            
        select_objects([Obj_main])
        O.object.duplicate()
        Obj_cutbody = C.object      #Obj main will be reduced to just the belly (using the goal VG), the Obj_cutbody is the body without the belly.
        for i in [Obj_main, Obj_cutbody]:
            select_objects([i])
            O.object.mode_set(mode='EDIT')
            O.mesh.select_all(action='DESELECT')
            i.vertex_groups.active_index = VG_goal.index #even though modifiers have been applied, the total amount of vertex groups shouldn't have changed. To be safe, we could choose the new index by name this time though.
            O.object.vertex_group_select()
            if i == Obj_main:
                O.mesh.select_all(action='INVERT')
                O.mesh.delete(type='VERT')
            elif i == Obj_cutbody:
                i.vertex_groups.active_index = VG_anchor.index
                bpy.ops.object.vertex_group_deselect()
                O.mesh.delete(type='VERT')
            O.object.mode_set(mode='OBJECT')
            
        for i in vertex_VGs_belly:          #we need to know the VGs of both objects so we can make sure they still have the same names (for merging) later on
            for g in Obj_cutbody.vertex_groups:
                if i.index == g.index:
                    vertex_VGs_body = vertex_VGs_body + [g]
                    break
                    
    print('    ... some other stuff again')
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        ###Copying SB and any Vertex Weight modifiers to Obj_main (they have been applied earlier as well). We can't use the copy-attributes addon, because for some reason it doesn't copy the *settings* of a softbody mod. Instead, we'll use the default "link modifiers" option, and delete all other useless modifiers.             
        select_objects([Obj_original, Obj_main])
        O.object.make_links_data(type='MODIFIERS')
        select_objects([Obj_main])
        for mods in Obj_main.modifiers:
            if mods.type not in ["SOFT_BODY", "VERTEX_WEIGHT_EDIT", "VERTEX_WEIGHT_MIX", "VERTEX_WEIGHT_PROXIMITY"]:    #possible bug happening here since list will get smaller while the loop is still running. Didn't test it though.
                O.object.modifier_remove(modifier = mods.name)         
            if mods.type == 'SOFT_BODY':
                    ModSB_temp = mods
                    ModSB_temp.show_viewport = False
        ModSB_temp.settings.collision_collection   = Coll_mddcollision_objs   #will now use the mdd_collision objects instead of the originals
        if ModSB_temp.settings.goal_default != 1 or ModSB_temp.settings.goal_max != 1:
            print("NOTE: The Default or Max goal value of your softbody wasn't set to 1, so the script assumed those numbers anyway. It needs those values to work properly. You can ignore this message.") 
        ModSB_temp.settings.goal_default           = 1
        ModSB_temp.settings.goal_max               = 1     #both values need to be turned to 1, otherwise the "anchor points" with a weight of 1 we created will be affected by the softbody mod and thus lose their purpose.
        ModSB_temp.show_viewport = True     #if it's hidden at this point no bakes will happen for whatever reason                           
        select_objects([Obj_main])
    print('Finished the Preparing.')

with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):

    ############Creating 2 duplicates of the selected objects so we don't mess up the originals
    #and assign them to variables
    O.object.duplicate()
    Obj_realmain = C.object                      
     
    
    
    #assigning the softbody-mod to a variable for easy referencing
    for mods in Obj_realmain.modifiers:         
        if mods.type == 'SOFT_BODY':
            ModSB_realmain = mods           #the softbody-modifier of the SB_dummy. Note however, that each time we create a new duplicate for baking, we must also assign its softbody modifier to a new variable since this one refers specifially to the SB_dummys SBmod. We could just work with it's name instead but that doesn't feel clean.
        break

    #immediately hiding the SB-mod.
    hide_mods(object = Obj_realmain, hide = True, modifier_list = [ModSB_realmain], noSB = False)  #If the softbody is unhidden when we don't need it, it will likely just cause issues, since it probably bakes a bit already. So, only unhide it when we actually want to bake it, and immediatly afterwards hide it again.


    if automatic_scaling == True:
        #since we don't want to mess up the original collision objects as well, we also have to duplicate them, and put the originals into a save collection. Something like this is also done almost immediatly after these lines, which is due to me adding this line of code later and not wanting to understand how these other lines worked exactly.
        Coll_realcollision_objs = create_collection("actual original coll_obs", avoid_duplicates = True)
        link_objects(ModSB_realmain.settings.collision_collection.objects, Coll_realcollision_objs)
        select_objects(Coll_realcollision_objs.objects)
        O.object.duplicate()
        L_duplcollision_objs = C.selected_objects
        link_objects(C.selected_objects, ModSB_realmain.settings.collision_collection) #selected objects are the duplicates.
        
        for i in [Obj_realmain]+list(L_duplcollision_objs):
            for e in [0,1,2]:
                i.lock_scale[e] = False       #if scaling is locked we obviously can't scale them
        select_objects([Obj_realmain]+list(L_duplcollision_objs))
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)    #if the locations aren't at 0 0 0, the scaling will lead to different locations than the originals later on.
        
        select_objects([Obj_realmain]+list(ModSB_realmain.settings.collision_collection.objects))
        h_thickness = 0       #while we could technically scale our objects to extreme values, we can't forget that the thickness of the collision objects needs to be scaled as well. However, they have a maximum value, which is 1 (1 meter). So we have to find out what the highest scale is at which the highest thickness just reaches 1.
        for i in ModSB_realmain.settings.collision_collection.objects:
            if i.collision.thickness_outer > h_thickness:
                h_thickness = i.collision.thickness_outer
            if i.collision.thickness_inner > h_thickness:
                h_thickness = i.collision.thickness_inner
        max_scale = 1/h_thickness
        #Some pivot points, like invidual origins, give wrong results. Using the 3D Cursor works though.
        scale_orig_p_point = C.scene.tool_settings.transform_pivot_point
        C.scene.tool_settings.transform_pivot_point = 'CURSOR'

        bpy.ops.transform.resize(value=(max_scale,max_scale,max_scale))
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        for i in ModSB_realmain.settings.collision_collection.objects:
            i.collision.thickness_outer = i.collision.thickness_outer * max_scale
            i.collision.thickness_inner = i.collision.thickness_inner * max_scale
    

    
    #also set the parent collection of Obj_realmain as the active one, otherwise problems might appear:
    C.view_layer.active_layer_collection = find_viewlayer_collection(Obj_realmain.users_collection[0].name)
     
    
    ###now also the collision objects, put them into a new, temporary collection:
    #but first create the final collections:
    Coll_main = create_collection('SACS_script_results', parent_collection = desired_target_collection, avoid_duplicates = True)
    Coll_sub  = create_collection('frames '+str(true_first_frame)+'-'+str(last_frame), parent_collection = Coll_main, avoid_duplicates = False)
    Coll_collision_objs = create_collection('orig collision objs', parent_collection = master_collection, avoid_duplicates = True)
    link_objects(ModSB_realmain.settings.collision_collection.objects, Coll_collision_objs) #function unlinks them from all previous collections, meaning they're not inside the collision collection anymore
    #########################################################################
    
    ##setting up datapaths for the mdd-files that this script will create####
    blend_file_path = D.filepath
    directory = os.path.dirname(blend_file_path)
    target_file_calc = os.path.join(directory, 'single_frame_bakes_calc.mdd')
    target_file_col  = os.path.join(directory, 'temp collision objects')
    #########################################################################
    
    
    ############scaling the keyframes of (almost?) ALL objects###############   
    stretch_time(time_stretch_multiplier)
    #########################################################################


    ############creating the first import frame##############################
    #This scipt uses the finished bake of the previous frame for the softbody sim of the current frame, but since we don't have a bake at the beginning we simply use the original shape at that frame, and for that it needs to be exported into an .mdd
    select_objects([Obj_realmain])
    O.export_shape.mdd (filepath = target_file_calc, frame_start = first_frame*time_stretch_multiplier, frame_end = first_frame*time_stretch_multiplier)
    #########################################################################


    ###creating the "permanent" duplicate that will show the final result#############
    #since we bake a softbody sim for each frame, we also need to give those finished bakes /shapes to an object on that frame to actually see it in the final animation. The "permanent duplicate" is that object, it gets more and more frames imported.
    C.scene.frame_set(first_frame * time_stretch_multiplier)
    O.object.object_duplicate_flatten_modifiers() #that's the function of the "Corrective Shape Keys" add-on that creates a static copy of your object.
    Obj_final = C.selected_objects[0]  #(should be the only selected object if the script worked until now)
    vertindex_calibrate("transfer_cSK", n_cSK, Obj_final, Obj_realmain)    #duplicate_flatten will lead to the new object having no shapekeys
    

    first_frame = first_frame + 1
    time_average = time.time()
    helper_start_f = true_first_frame
    time_5frame_average = time.time()
#print("time_average:",time_average)
#########################################################################

########################the big for-loop, repeats until every frame has been baked and put into keyframes.############
for x in range(last_frame - first_frame + 1):
    
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        temp_col_objects = duplicate_with_cut_keyframes(target_file_col, Coll_collision_objs.objects, [(first_frame) * time_stretch_multiplier, (first_frame) * time_stretch_multiplier + 1], 1, mod_list = [])
        link_objects(temp_col_objects, ModSB_realmain.settings.collision_collection)
        
        
        C.scene.frame_set(first_frame* time_stretch_multiplier)  #sets the current frame to one of the scaled keyframes of the main animation object
        time_framebake = time.time()
        print("time_framebake:",time_framebake)
        
    print('\nCurrent frame:', int((C.scene.frame_current / time_stretch_multiplier)))
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        select_objects([Obj_realmain])
        O.object.object_duplicate_flatten_modifiers() #creating the (temporary) keyframe-specific duplicate through the "corrective shapekeys" addon. The duplicate gets selected automatically when doing this
        Obj_duplmain = C.selected_objects[0] #(should be the only selected object)
        vertindex_calibrate("transfer_cSK", n_cSK, Obj_duplmain, Obj_realmain)
        select_objects([Obj_duplmain])    #dont know if vi_calibrate() saves selection, need to check
        O.import_shape.mdd(filepath=target_file_calc, frame_start=(first_frame - 1) * time_stretch_multiplier, frame_step = 1) #imports the "single_frames_bakes.mdd" on the duplicated object, with stretching of the keyframes according to the time stretch multiplier. This means that even when using no softbody modifier at all, it should still be back to its default shape at the last frame again, as the previous frame is only imported as a shapekey, whose value is keyframed to go down to 0 at the last frame.
        select_objects([Obj_realmain, Obj_duplmain])
        O.object.copy_obj_wei()                       #copying vertex weigths (through that 'Copy Attributes Menu' addon)
        O.object.make_links_data(type='MODIFIERS')    #copying modifiers
        
        for mods in Obj_duplmain.modifiers:         
            if mods.type == 'SOFT_BODY':
                ModSB_temp = mods                     #ModSB_realmain (without _t) specifically refers to the SB mod of the original SB-dummy, meaning we have to assign the SB-mod of the temporary duplicate to another, temporary variable to be able to refer to it.
                break
        hide_mods(object = Obj_duplmain, hide = True, modifier_list = [ModSB_temp], noSB = False) #as stated before, having a softbody mod unhidden when we don't use it has only possible negative results.
        
        ######
        #the next part is for vertex group modifiers that the user might have on his softbody_dummy. Good example is a vertex weight proximity modifier - VWP. Because you can't put it before the SB-mod in the mod-stack you can't effectively use them together for instance. We solve that by simply applying the VWP at the beginning of a frame, so the SB-mod *has* to use the modified vertex group. It doesn't affect the original softbody_dummy in any way (if I didn't mess up), which may be needed in other cases, but that will have to be dealed with when it's needed.
        
        select_objects([Obj_duplmain])
        O.object.duplicate()
        Obj_vw_duplicate = C.object
        Obj_vw_duplicate.active_shape_key_index = 1 #just to be sure. VWP uses the currently selected shapekey with a value of 1 as its base and ignores all others.
        bpy.ops.object.modifier_remove(modifier=ModSB_realmain.name) #dont want to have any possible baked frames here.
        delete_basis_SK(Obj_vw_duplicate)
        select_objects([Obj_realmain, Obj_vw_duplicate])
        O.object.copy_obj_wei()             #don't know why I do that but I feel like i have to do that.
        apply_modifiers(Obj_vw_duplicate) #we can apply all modifiers - including the VWP to change Vertex weights. The only purpose of this object is to copy its applied vertex groups to the actual baking duplicate.
        
        
            
        #select_objects([Obj_vw_duplicate, Obj_realmain]) #if using a VWP global influence of 1 the original VG gets overwritten completely each frame, so there's no need to give it back to the main_ani, we only need to give it to the baking temp. duplicate as this one actually has to use it. Yes, I know, a value of 1 isn't always going to be the case but that's it for now.
        select_objects([Obj_vw_duplicate,Obj_duplmain])
        O.object.copy_obj_wei()
        if animate_vgroups == True: #small part to copy and keyframe the new vertex weights to the final result. If the object already has vertex-groups with the same names, they'll just get replaced but keep their keyframes, which is exactly what we need.
            select_objects([Obj_vw_duplicate, Obj_final])
            bpy.ops.object.copy_obj_wei()
            select_objects([Obj_final])
            for i in range(len(list(C.object.vertex_groups))):
                C.object.vertex_groups.active_index = i
                bpy.ops.anim.insert_keyframe_animall()
        select_objects([Obj_vw_duplicate])
        O.object.delete(use_global=False)
        
        ####
        
        #change its softbody timerange of baking:
        select_objects([Obj_duplmain])
        SB_keyframe_insert(((first_frame-1) * time_stretch_multiplier), Obj_duplmain)
        ModSB_temp.point_cache.frame_start = (first_frame-1) * time_stretch_multiplier - 1  #as explained before, since we keyframe the goal value to be exactly 1 at the starting frame, we then actually start the bake one frame earlier, as it wouldn't have an effect otherwise.  
        ModSB_temp.point_cache.frame_end = first_frame * time_stretch_multiplier
        
  
        #bake it:    
        hide_mods(object = Obj_duplmain, hide = False, modifier_list = [ModSB_temp], noSB = False)  #A softbody mod cannot bake (and!) show its results if it is hidden, so we unhide it. It does not need to be hidden afterwards again, since the object will just be deleted instead of reused.
        override = {'scene': C.scene, 'active_object': Obj_duplmain, 'point_cache': ModSB_temp.point_cache}
        O.ptcache.bake(override, bake=True)
           
        #set the baked tempory duplicate as active again:
        select_objects([Obj_duplmain])
      
        #export the final baked frame into an .mdd and import it on the permanent duplicate:
        O.export_shape.mdd (filepath = target_file_calc, frame_start = first_frame * time_stretch_multiplier, frame_end = first_frame * time_stretch_multiplier)
        select_objects([Obj_final])
        O.import_shape.mdd(filepath=target_file_calc, frame_start = (first_frame) *time_stretch_multiplier, frame_step=time_stretch_multiplier)
        
        #delete the temporary duplicate again, a new one will be created in the next round of this for-loop.
        select_objects([Obj_duplmain])
        O.object.delete(use_global=False)
        
        #delete temp collision objects
        for i in ModSB_realmain.settings.collision_collection.objects:
            select_objects([i])
            O.object.delete(use_global=False)
        
    #do the remaining stuff    
    ##print('\nFrame ',first_frame,' finished baking\n')
    first_frame = first_frame + 1
    print('Frame needed %s seconds to finish baking.' % int((round(((time.time() - time_framebake)),0))))
    time_framebake_average = round(((time.time() - time_average)/(first_frame - true_first_frame - 1)),0) #in seconds
    print('Current average baking time per frame: %s seconds' % (time_framebake_average))
    if helper_start_f+2 == first_frame:                      #every 5 frames, and once at the beginning, the average time between those 5 frames will be used to estimate the remaining time.
        helper_start_f = helper_start_f + 5
        if first_frame - true_first_frame == 2:
            time_5framebake_average_print = round((time.time() - time_5frame_average),0) #in seconds
        else:
            time_5framebake_average_print = round(((time.time() - time_5frame_average)/5),0) #in seconds
        print('***Estimated remaining time: %s minutes' % round(((last_frame - first_frame+1)*time_5framebake_average_print/60),2))
        time_5frame_average = time.time()
    
    if (time.time()-time_script_begin) >= max_baking_time and not max_baking_time == 0:
        print('\n'+print_symbol_hash + 'Runtime has reached specified limit of ' + str(round((max_baking_time/60),2)) + 'minutes; finishing script early \nlast baked frame:', first_frame-1,   '\n'+print_symbol_hash )
        last_frame = first_frame - 1
        break
    if max_baking_time != 0:
        print('Script ends in either '+str(last_frame - first_frame)+' frames\nor '+str(round(((max_baking_time  - (time.time() - time_script_begin))/60),1))+'minutes')
    elif max_baking_time == 0:
        print('Script ends in '+str(last_frame - first_frame + 1)+' frames\n')
        
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
    
    
    
    Obj_final.name = "calc"



    L_final_objs = [Obj_final]       #all objects inside this list will be linked to our new collection later. They'll also be unlinked from their current linked collection, which should only be one.

    if main_anim_copy == True:
        target_file_ma_copy = os.path.join(directory, 'main_anim_copy with baked frame')
        select_objects([Obj_realmain])
        O.export_shape.mdd (filepath = target_file_ma_copy, frame_start = last_frame + 1, frame_end = anim_last_frame)
        O.object.object_duplicate_flatten_modifiers()
        main_anim_copy = C.selected_objects[0]
        main_anim_copy.name = Obj_realmain.name + ' baked copy'
        O.import_shape.mdd(filepath=target_file_ma_copy, frame_start = last_frame + 1, frame_step=1) 
        select_objects([Obj_final])
        O.export_shape.mdd (filepath = target_file_ma_copy, frame_start = last_frame, frame_end = last_frame)
        select_objects([main_anim_copy])
        O.import_shape.mdd(filepath=target_file_ma_copy, frame_start = last_frame, frame_step=1) 
        L_final_objs = L_final_objs + [main_anim_copy]
        select_objects([Obj_realmain, main_anim_copy])
        O.object.copy_obj_wei()



    link_objects(L_final_objs, Coll_sub, [])

   
    
    #put the duplicates of the actual original collision objects into the collision collection again. #yes I know that this is confusing since they aren't the actual duplicates if automatic_scaling is enabled, I just wanted to add some lines of code without having to revisit the whole script again.
    link_objects(Coll_collision_objs.objects, ModSB_realmain.settings.collision_collection)

    #maybe we don't have to link them at all if the originals remained in the original softbody collision collection?

    #getting rid of all the stuff we did if the scaling-option is enabled.
    if automatic_scaling == True:
        select_objects([Obj_realmain]+list(L_duplcollision_objs)+[Obj_final])
        bpy.ops.transform.resize(value=(1/max_scale,1/max_scale,1/max_scale))
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        select_objects([Obj_realmain] + list(L_duplcollision_objs))
        link_objects(Coll_realcollision_objs.objects, ModSB_realmain.settings.collision_collection)
        O.object.delete(use_global=False)
        bpy.data.collections.remove(Coll_realcollision_objs)
        C.scene.tool_settings.transform_pivot_point = scale_orig_p_point
    else:
        select_objects([Obj_realmain]) #remember that this is a duplicate of the original object, meaning we can safely delete it.
        O.object.delete(use_global=False)


    bpy.data.collections.remove(Coll_collision_objs)   #removes the temporary needed collection for the collision objects. Sidenote: removing a collection will unlink all collections inside from your current scene.
   
if easy_mode == True:
    print('easy_mode = True    => Cleaning up stuff...')
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        ###resetting SB_goal VG to original values
        VWM_mod = Obj_main.modifiers.new(name = "resetting SB-goal", type = 'VERTEX_WEIGHT_MIX')   #later change this to be for the finished/fused model
        VWM_mod.vertex_group_a = VG_goal.name
        VWM_mod.vertex_group_b = VG_goal_backup.name
        VWM_mod.mix_mode = 'SET'    #sets mix mode to "Replace"
        VWM_mod.mix_set = 'ALL'     #sets mix set to "All"; the default one ("VGroup A and B") does not affect vertices that aren't assigned to a VG. However, using this option will lead to *all* vertices being assigned to VG A, if only with a weight of 0.
        #We should refrain from using VWE mods to remove those 0-weight vertices, since the original vertex group might have had vertices with a weight of 0 as well.
        #Solution: select all vertices of the backup, invert selection and unassign those vertices from the original VG_goal
        select_objects([Obj_main])
        O.object.modifier_apply(modifier=VWM_mod.name)
        O.object.mode_set(mode='EDIT')
        O.mesh.select_all(action='DESELECT')
        Obj_main.vertex_groups.active_index = VG_goal_backup.index
        O.object.vertex_group_select()
        O.mesh.select_all(action='INVERT')
        Obj_main.vertex_groups.active_index = VG_goal.index
        O.object.vertex_group_remove_from()
        O.object.mode_set(mode='OBJECT')
        
        #we first need to delete the goal VG and its backup from the Obj_cutbody object, because the VG_goal and VG_goal_backup refer to the ones of Obj_main. VG_goal will only get deleted from Obj_cutbody.
        select_objects([Obj_cutbody])
        Obj_cutbody.vertex_groups.active_index = Obj_cutbody.vertex_groups[VG_goal_backup.name].index
        O.object.vertex_group_remove(all=False, all_unlocked=False)
        Obj_cutbody.vertex_groups.active_index = Obj_cutbody.vertex_groups[VG_goal.name].index
        O.object.vertex_group_remove(all=False, all_unlocked=False)

        select_objects([Obj_main])
        Obj_main.vertex_groups.active_index = VG_goal_backup.index
        O.object.vertex_group_remove(all=False, all_unlocked=False) #deletes the backup VG

        ###removing the SB_mod from Obj_main
        for mods in Obj_main.modifiers:         
            if mods.type == 'SOFT_BODY':
                ModSB_main = mods            #for some reason the variable stopped referencing this mod halfway through, so we'll have to assign it once again.
        ModSB_main.name = 'You can delete this modifier'
        try:
            O.object.modifier_remove(modifier = ModSB_main.name)
        except:
            print('A UnicodeDecodeError happened when trying to remove the softbody-modifier of the result. The result will continue as normal, but you will have to remove the modifier yourself - it is not required however')    #I GOT NO FUCKING IDEA WHY IT HAPPENS SOMETIMES.
        
        ###giving the finished/animation of the calc result
        select_objects([Obj_final])
        O.export_shape.mdd (filepath = target_file_calc, frame_start = true_first_frame, frame_end = true_last_frame)
        O.object.delete(use_global=False)
        Obj_final = Obj_main

        select_objects([Obj_final])
        O.object.duplicate()
        vi_belly = C.selected_objects[0]
        vi_belly.name = "VI_belly"
        select_objects([Obj_final])
        
        O.object.mode_set(mode='EDIT')
        Obj_final.active_shape_key_index = 0            #I dont fucking understand why, but whenever I tried to remove the shapekeys, it didn't get the Basis Shape, but the one of the last frame. Only way I got it to work is to go into edit mode and select the Basis shapekey in there.
        O.object.mode_set(mode='OBJECT')
        Obj_final.shape_key_clear()        
        O.import_shape.mdd(filepath=target_file_calc, frame_start = true_first_frame)
        

        ###fusing the two body parts together again
        vertindex_calibrate("transfer_cSK", n_cSK, Obj_final, vi_belly)
        select_objects([Obj_final])
        for i in range(len(vertex_VGs_belly)):  #first making sure Obj_final's and Obj_cutbody's single-vertex-VGs have the same names so they can be merged. Attention: Calling Obj_cutbody variables after joining can lead to crashs.
            vertex_VGs_body[i].name = vertex_VGs_belly[i].name
        select_objects([Obj_final, Obj_cutbody])

        O.object.join()
        O.object.mode_set(mode='EDIT')
        for i in vertex_VGs_belly:      #goes through the VGs that now contain the same two vertices (of both objects) each one by one, and merges those two vertices.
            O.mesh.select_all(action='DESELECT')
            Obj_final.vertex_groups.active = i
            O.object.vertex_group_select()
            O.mesh.remove_doubles(threshold=0.0001)
        O.object.mode_set(mode='OBJECT')

        for i in vertex_VGs_belly:
            Obj_final.vertex_groups.remove(i)
        Obj_final.vertex_groups.remove(VG_anchor)
        
        
        ###cleaning up 
        Obj_final.name = 'calc'
        vertindex_calibrate("reset_vi", n_cSK, Obj_final, Obj_VI_main)
        vertindex_calibrate("delete_cSK", n_cSK, Obj_final)
        link_objects([Obj_final], Coll_sub, [])
        select_objects(L_mddcollision_objs + [vi_belly] + [Obj_VI_main])
        O.object.delete(use_global=False)
        D.collections.remove(Coll_mddcollision_objs)
        
with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
    ModSB_original.show_viewport = show_viewport_of_SB_orig #resetting to the state it had at the beginning
    C.view_layer.active_layer_collection = ori_av_layercoll
    C.scene.frame_set(default_frame)  #small note, just noticed that using this line will make your current active object not be active anymore.
    select_objects([Obj_final])

    time_script_end = time.time()
print('\n\nScript took %s minutes to finish.' % (round(((time_script_end - time_script_begin)/60),2)))
print('One frame needed %s seconds on average to finish baking.' % (round(((time.time() - time_average)/(last_frame-true_first_frame)),1)))


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
