VERSION 1.53.2.1 DOES NOT WORK WITH BLENDER VERSION 2.83 OR LOWER.




# Cardboy0s-SACS


Due to me not wanting to copy everything everywhere, visit https://docs.google.com/document/d/1rpJIQqvXcGL9UN-JYzqRKVHk8xaMxgCKM0UYLyqDW_A/edit for tutorials and tips concerning this script.

As the name says, it's for softbodies in Blender, more specifically animated ones, be it through modifiers, transforms or shapekeys. If you use a default softbody with animations, that softbody will interpret these animations as external forces and thus deform even if there's no collision object anywhere, and for instance try to take on the shape of the Basis shapekey. By using this script, your softbody will animate like it originally did before (depending on your values maybe still a tiny bit different though), and only deform when collision objects collide with it. However your softbody will not be able to work with velocities as each frame gets baked in a seperate simulation for more than one frame, so velocities of previous frames will not be saved. In other words, it won't show gravity acceleration for instance. It's main purpose is for deforming your softbody to get bulges or dents, not make it jiggle or wobble.
All the important stuff is written in the script-file itself, so technically you don't need this README.

Requires the 3 addons "NewTek MDD format", "Corrective Shape Keys" and "Copy Attributes Menu". 
The finished result will be completely animated by keyframed shapekeys. You don't want your softbody to have any modifiers that aren't needed for the softbody modifier ("beauty modifiers"), like corrective smooth or similar stuff, and instead use another script by me, the "retroactive beautifier" (also found on this github profile) to apply those retroactively, using the finished result and your original animation. You don't need this for modifiers like subdiv, but if you want to use corrective smooth, Laplacian deform, etc. that require a base shape for reference, you can use it to have that base shape change every frame to be that of the original animation, meaning the whole original animation will actually be the base for these modifiers on your result.

Also feel free to ask me questions, report bugs or do other stuff on my twitter: https://twitter.com/cardboy0 (or use this github of course)
