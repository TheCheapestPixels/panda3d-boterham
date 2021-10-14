import json
import os
import bpy
import blend2bam.blender_script_common as common #pylint: disable=import-error,wrong-import-position
from blend2bam.blend2gltf.blender28_script import (
    export_physics,
    fix_image_uri,
    add_actions_to_nla,
    prepare_meshes,
)


def export_gltf(settings, src, dst):
    print('Converting .blend file ({}) to .gltf ({})'.format(src, dst))
    dstdir = os.path.dirname(dst)
    os.makedirs(dstdir, exist_ok=True)
    common.make_particles_real()
    add_actions_to_nla()
    prepare_meshes()

    print("doing custom shiiii!")

    bpy.ops.export_scene.gltf(
        filepath=dst,
        export_format='GLTF_EMBEDDED' if settings['textures'] == 'embed' else 'GLTF_SEPARATE',
        export_cameras=True,
        export_extras=True,
        export_yup=False,
        export_lights=True,
        export_force_sampling=True,
        export_apply=True,
        export_tangents=True,
        export_animations=settings['animations'] != 'skip',
    )

    with open(dst) as gltf_file:
        gltf_data = json.load(gltf_file)

    export_physics(gltf_data)
    if settings['textures'] == 'ref':
        fix_image_uri(gltf_data)

    with open(dst, 'w') as gltf_file:
        json.dump(gltf_data, gltf_file, indent=4)


if __name__ == '__main__':
    common.convert_files(export_gltf, 'gltf')
