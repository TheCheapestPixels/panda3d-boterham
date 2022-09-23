import os
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld

from .terrain import make_terrain
from .property_logic import tags_as_bullet
from .property_logic import tags_as_node_function


def boterham_load_model(filename):
    root = loader.load_model(filename)
    # Load links
    # TODO: Make recursive
    loaded = {}
    for child in root.find_all_matches('**/=__linked_file'):
        path = child.get_tag('__linked_file')
        path = os.path.dirname('./'+filename)+path
        nodename = child.get_tag('__linked_node')
        if path in loaded:
            file = loaded[path]
        else:
            file = loaded[path] = boterham_load_model(path)
        node = file.find('**/'+nodename)
        if not node:
            raise Exception("Couldn't find nodepath " + nodename + " in blend " + path)
        instance = node.copy_to(child.parent)
        instance.set_transform(child.get_transform())
        child.detach_node()

    # Setup heightmap
    for child in root.find_all_matches('**/=__make_terrain'):
        filepath, height = child.get_tag('__make_terrain').split(',')
        terrain_root = make_terrain(filepath, int(float(height)))
        terrain_root.wrt_reparent_to(child.parent)
        terrain_root.set_pos(terrain_root, child.get_pos())
        child.detach_node()

    tags_as_bullet(root)
    tags_as_node_function(root)

    return root

def make_bullet_world(root, gravity=Vec3(0,0,-9.81), debug=False):
    world = BulletWorld()
    world.set_gravity(gravity)
    for bullet_type in [
        "BulletRigidBodyNode", "BulletCharacterControllerNode", "BulletVehicle",
        "BulletConstraint", "BulletGhostNode", "BulletSoftBodyNode",
    ]:
        for nodepath in root.find_all_matches("**/+"+bullet_type):
            world.attach(nodepath.node())

    if debug:
        debug_node = BulletDebugNode("Bullet Debug")
        debug_node.show_wireframe(True)
        debug_node.show_constraints(True)
        debug_node.show_bounding_boxes(False)
        debug_node.show_normals(False)
        debug_np = root.attach_new_node(debug_node)
        debug_np.show()
        world.set_debug_node(debug_np.node())

    return world
