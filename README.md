# boterham
`boterham` is a custom pre-and-post processor for `blend2bam`, which is a CLI tool to convert Blender blend files to Panda3D BAM files.

Since a lot of my projects often end up with some bam parser I decided to make a more definitive one.
Pre-processing revolves around automatically setting up custom properties to nodes in blend files based on certain characteristics applying destructive modifiers.
Post-processing will then read all the custom properties as tags in panda3d and alter the nodes. Property names could mirror function names.
I might add a generic pre-loader for setting up things on game load that can not be saved as a BAM file.

This place could also serve as a testbed for new blend2bam features.

## Don't use this yet.


### Currently implemented:
* nothing

### Dream features:
* flattening
* merged collision shapes
* displacement modifiers as ShaderTerrainMesh
* automatic LODNodes using the Decimation modifier
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
