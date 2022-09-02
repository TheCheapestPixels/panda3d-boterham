# boterham
`boterham` is a custom pre-and-post processor for `blend2bam`, which is a CLI tool to convert Blender blend files to Panda3D BAM files.

Since a lot of my projects often end up with some bam parser I decided to make a more definitive one.
Pre-processing revolves around automatically setting up custom properties to nodes in blend files based on certain characteristics applying destructive modifiers.
Post-processing will then read all the custom properties as tags in panda3d and alter the nodes. Property names could mirror function names.
I might add a generic pre-loader for setting up things on game load that can not be saved as a BAM file.

This place could also serve as a testbed for new blend2bam features.

This project started by ripping everything out of blend2bam. For this reason it should carry blend2bam's license for ever and ever. Any level of professionality in this project is thanks to Moguri.

It works just like blend2bam. After installing do ```boterham myblendfile.blend newbamfile.bam```

## Currently implemented:
### Calling NodePath functions and replace with PandaNodes using Custom Properties
Adding a custom property in blender whose name starts with the symbol `$` will run it as a function on the NodePath. For example adding `$reparent_to` or `$flatten_strong`. You can pass arguments to this function using a dict as property value as followed: `"extra_args":[some_value]`. This is evaluated as JSON.

A property starting with `$node().` will run the function on the first attached PandaNode. For example on a DirectionalLight one could do `$node().set_color` with value `"extra_args":[[1,0,0,1]]` to make it shine red.

This is especially useful in combination with node replacement, by starting a property name with the symbol `+`. For example on an empty, one could add the property `+SequenceNode` to turn it into a sequence node. Add another property `$node().loop` to make it start playing in an endless loop.

An argument that starts with the symbol `@` will be replaced with the first nodepath found through `render.find().` For example property `$reparent_to` with value `"extra_args":["@**/Camera"]` will reparent the nodepath to whatever node in the scene is called Camera.

### Empty to CollisionShape
Using the property `+CollisionNode` now iterates over all children and looks for any of the `+CollisionShape`s (`+CollisionSphere`, `+CollisionBox`, etc.) and will try to make sense of them based on their transforms.
Setting these on sphere-, box- or arrow empties in blender make for nice representations. Sadly blender does not have a capsule empty but one can imagine it being sliced out of a sphere like a cookie-cutter.
`+CollisionPolygon` only works partially/experimentally. It's better to use the following implemented technique:
NOTE: Contrary to panda3d's defaults, boterham sets each CollisionNode's CollideMask to 0 meaning they don't do anything without first setting a CollideMask. You could set this manualy with the `$set_collide_mask` property if you wanted to.

### Decending CollisionPolygons.
Adding the property `geom_to_collision_polygon` will recursively copy all children's GeomNodes as CollisionPolygons. Tip: Use `$flatten_strong` to combine shapes.

### Automatic LODNodes using the Decimation modifier
Add a Decimate modifier an name it `LOD_N`, where N is the number of LOD levels you want.
Set the modifiers ratio to be the furthest LOD.
Manual LODNodes was already possible by placing the property `+LODNode` (turning its children into switches)
Note: at the moment subdivision surface modifiers are applied AFTER LOD processing, so apply them manually for now.

### Instances from Geometry Nodes
Instances created with a Geometry Node modifier (Blender>3.00) are made real and exported.

### Wireframe
When you check the "wireframe" option in the viewport display menu in the object tab, boterham duplicates the object and removes all the faces, leaving behind the edges.
These edges will be colored by the object color, as set in the same menu.

## Model loader
Some features require you to use the boterham model loader so it can set up parts of the scenegraph that don't get stored into a bam.
It should be a drop-in replacement for loader.load_model like so:
```
from boterham.loader import boterham_load_model
from direct.showbase.ShowBase import Showbase

base = ShowBase()
boterham_load_model('my_model.bam').reparent_to(render)
render.ls()
```
This would enable you to use the following features:

### Displacement modifier as ShaderTerrainMesh
Adding a Z-up `Displacement` modifier to a subdivided plane called `ShaderTerrainMesh` will create a Panda3D `ShaderTerrainMesh` with corresponding `BulletHeightfieldShape` on load.
I suggest you use a strength of 128 on a plane scaled 1024x1024 untill this system is further fleshed out.
IMPORTANT: In blender, set the displacement map texture's `color space` to `Linear`.
Now you can texture paint the heightmap in blender using greyscale brushes. Fun!

### External linking
Externally linked collections are turned into empties tagged with their original filename and collection.
Then load the bam like so, it will look for the linked nodes in relative bams:

Note: At the moment the linked collection should begin with one root node (like an empty) with the same name as the collection.
This is because blender links collections which are not exported to gltf.
Also this behavior should be optional but isn't at the moment. All linked instances will turn to tagged empties when using boterham. Sorry!

## Dream features:
* store vertex groups as list of vertex indices
* apply mirror and array modifiers as separated and recentered meshes
* bake procedural textures as pbr material
* handle modifiers with regards to shapekeys (convert each shapekey to model, apply modifiers, parent back as shapekey)
* expose objects to bones
* convert object animation to armature animation
* mesh to waypoint
* who knows what else!

### Note
Some assumptions are being made and not all legacy blend2bam functionality works. It supports version >3.0 of blender.
