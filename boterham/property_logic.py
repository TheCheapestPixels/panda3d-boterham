import sys
import json
import panda3d.core

from .collisions import set_collisions, set_collision_shapes
from .bullet import set_bullet_shapes


def set_lod_switches(nodepath):
    furthest = 1024
    step_size = furthest/len(nodepath.get_children())
    into, outto = furthest, furthest-step_size
    for c, child in enumerate(nodepath.get_children()):
        nodepath.node().add_switch(into, outto)
        into = outto
        outto /= 2
    furthest_out = nodepath.node().get_out(0)
    nodepath.node().set_switch(0, furthest**4, furthest_out)

def read_args(root, value_raw):
    if value_raw == "None" or value_raw == '1' or value_raw == '1.0':
        return []
    extra_args = []
    try:
        value_json = json.loads('{'+value_raw+'}')
    except json.decoder.JSONDecodeError:
        print('error, json cant decode:', value_raw)
        sys.exit(1)

    if 'extra_args' in value_json:
        if type(value_json['extra_args']) == list:
            for arg in value_json['extra_args']:
                if type(arg) == str:
                    if arg[0] == '@':
                        found = root.find(arg[1:])
                        if found:
                            arg = found
                        else:
                            print('could not find {}'.format(arg))
                            sys.exit(1)
                if type(arg) == list:
                    arg = tuple(arg)
                extra_args.append(arg)
        else:
            print('extra_args of {} is not a list'.format(tag))
            sys.exit(1)
    return extra_args

def tags_as_nodepath_function(root, nodetype=panda3d.core.NodePath('nodepath')):
    funcs = dir(nodetype)
    custom_sort = [
        'wrt_reparent_to',
        'reparent_to',
        'flatten_strong',
    ]
    custom_sort.reverse()
    for s in custom_sort:
        funcs.remove(s)
        funcs.insert(0, s)

    for func in funcs:
        tag = '${}'.format(func)
        for nodepath in root.find_all_matches("**/="+tag):
            print(' Running NodePath function:',tag, nodepath)
            value_raw = nodepath.get_tag(tag)
            extra_args = read_args(root, value_raw)
            function = getattr(nodepath, func)
            function(*extra_args)
            nodepath.clear_tag(tag)
            nodepath.clear_python_tag(tag)

def tags_as_node_function(root, nodetype=panda3d.core.PandaNode('pandanode')):
    funcs = dir(nodetype)
    funcs.sort(key=lambda s: len(s))
    for func in funcs:
        tag = '$node().{}'.format(func)
        for nodepath in root.find_all_matches("**/="+tag):
            value_raw = nodepath.get_tag(tag)
            extra_args = read_args(root, value_raw)
            function = getattr(nodepath.node(), func)
            function(*extra_args)
            nodepath.clear_tag(tag)
            nodepath.clear_python_tag(tag)

def convert_to_class(root, nodepath, name, panda_node, replace=True):
    tag = '+{}'.format(name)
    value_raw = nodepath.get_tag(tag)
    extra_args = read_args(nodepath, value_raw)
    new_node = panda_node(nodepath.name) #, *extra_args)
    new_nodepath = nodepath.parent.attach_new_node(new_node)
    new_nodepath.set_transform(nodepath.get_transform())
    nodepath.clear_tag(tag)
    nodepath.clear_python_tag(tag)
    for key in nodepath.get_python_tag_keys():
        new_nodepath.set_python_tag(key, nodepath.get_python_tag(key))
    for key in nodepath.get_tag_keys():
        new_nodepath.set_tag(key, nodepath.get_tag(key))
    for child in nodepath.get_children():
        child.reparent_to(new_nodepath)
    if replace:
        nodepath.detach_node()
    tags_as_node_function(root, nodetype=new_node)
    return new_nodepath

def tags_as_class(root):
    panda_nodes = [
        "PandaNode", "DataNode", "MouseRecorder", "AnalogNode", "ButtonNode", "DialNode", "TrackerNode",
        "VirtualMouse", "MouseAndKeyboard", "MouseInterfaceNode", "DriveInterface,MouseSubregion",
        "Trackball", "ButtonThrower", "MouseWatcher", "Transform2SG", "InputDeviceNode", "LightNode",
        "AmbientLight", "CallbackNode", "ComputeNode", "LensNode", "Camera", "LightLensNode",
        "DirectionalLight", "PointLight", "SphereLight", "RectangleLight", "Spotlight", "LODNode",
        "FadeLODNode", "SelectiveChildNode", "SequenceNode", "SwitchNode", "UvScrollNode", "Fog",
        "GeomNode", "ModelNode", "ModelRoot", "PlaneNode", "PolylightNode", "PortalNode", "OccluderNode",
        "TextNode", "FrameRateMeter", "SceneGraphAnalyzerMeter", "RigidBodyCombiner",
        "ShaderTerrainMesh", "AnimBundleNode", "PartBundleNode", "Character", "CollisionNode",
        "CollisionVisualizer", "ParametricCurve", "PiecewiseCurve", "NurbsCurve", "HermiteCurve",
        "CubicCurveseg", "RopeNode", "SheetNode", "PGItem", "PGButton", "PGEntry", "PGVirtualFrame",
        "PGScrollFrame", "PGSliderBar", "PGWaitBar", "PGTop",
    ]
    for panda_node in panda_nodes:
        tag = '+{}'.format(panda_node)
        for nodepath in root.find_all_matches("**/="+tag):
            print(' Turn to PandaNode:',tag, nodepath)
            new_nodepath = convert_to_class(root, nodepath, panda_node, getattr(panda3d.core, panda_node))
            if panda_node == 'LODNode' or panda_node == 'FadeLODNode':
                set_lod_switches(new_nodepath)
            elif panda_node == 'CollisionNode':
                set_collision_shapes(new_nodepath)

def tags_as_bullet(root):
    bullet_nodes = [
        "BulletCharacterControllerNode", "BulletSoftBodyNode", #"BulletVehicle",
        "BulletBodyNode", "BulletRigidBodyNode", "BulletGhostNode",
    ]
    for panda_node in bullet_nodes:
        tag = '+{}'.format(panda_node)
        for nodepath in root.find_all_matches("**/="+tag):
            print(' Turn to bullet body:',tag, nodepath)
            new_nodepath = convert_to_class(root, nodepath, panda_node, getattr(panda3d.bullet, panda_node))
            set_bullet_shapes(new_nodepath)

def evaluate_property_logic(root):
    tags_as_class(root)
    tags_as_nodepath_function(root)
    set_collisions(root)
