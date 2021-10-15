# boterham
`boterham` is a custom pre-and-post processor for `blend2bam`, which is a CLI tool to convert Blender blend files to Panda3D BAM files.

Since a lot of my projects often end up with some bam parser I decided to make a more definitive one.
Pre-processing revolves around automatically setting up custom properties to nodes in blend files based on certain characteristics applying destructive modifiers.
Post-processing will then read all the custom properties as tags in panda3d and alter the nodes. Property names could mirror function names.
I might add a generic pre-loader for setting up things on game load that can not be saved as a BAM file.

This place could also serve as a testbed for new blend2bam features.

### Don't use this yet.
But if you do, it works just like blend2bam. After installing do ```boterham myblendfile.blend newbamfile.bam```

## Currently implemented:
### Calling functions and replace PandaNodes with Custom Properties
Adding a custom property in blender whose name starts with the symbol `$` will run it as a function on the NodePath. For example adding `$reparent_to` or `$flatten_strong`. You can pass arguments to this function using a dict as property value as followed: `"extra_args":[some_value]`. This is evaluated as JSON.

A property starting with `$node().` will run the function on the first attached PandaNode. For example on a DirectionalLight one could do `$node().set_color` with value `"extra_args":[(1,0,0,1)]` to make it shine red.

This is especially useful in combination with node replacement, by starting a property name with the symbol `+`. For example on an empty, one could add the property `+SequenceNode` to turn it into a sequence node. Add another property `$node().loop` to make it start playing in an endless loop.

An argument that starts with the symbol `@` will be replaced with the first nodepath found through `render.find().` For example property `$reparent_to` with value `"extra_args":[@**/Camera]` will reparent the nodepath to whatever node in the scene is called Camera.

### Automatic LODNodes using the Decimation modifier
Add a Decimate modifier an name it `LOD_N`, where N is the number of LOD levels you want.
Set the modifiers ratio to be the furthest LOD.
Note: at the moment subdivision surface modifiers are applied AFTER LOD processing, so apply them manually for now.


## Dream features:
* merged collision shapes
* displacement modifiers as ShaderTerrainMesh
* better handle linked instances
* better handle textures
* bake procedural textures as pbr material
* handle modifiers with regards to shapekeys
* convert object animation to armature animation
* mesh to waypoint
* edges as drawn with LineSegs
* who knows what else!


### Note
Some assumptions are being made and not all blend2bam functionality work. It supports version >2.8 of blender only using pbr materials.
