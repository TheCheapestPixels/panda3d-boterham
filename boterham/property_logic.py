import sys
import json
import panda3d.core


def read_args(root, value_raw):
    if value_raw == "None" or value_raw == '1':
        return []
    extra_args = []
    value_json = json.loads('{'+value_raw+'}')
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
                extra_args.append(arg)
        else:
            print('extra_args of {} is not a list'.format(tag))
            sys.exit(1)
    return extra_args

def tags_as_nodepath_function(root, nodetype=panda3d.core.NodePath('nodepath')):
    funcs = dir(nodetype)
    funcs.sort(key=lambda s: len(s))
    for func in funcs:
        tag = '${}'.format(func)
        for nodepath in root.find_all_matches("**/="+tag):
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
        "PGScrollFrame", "PGSliderBar", "PGWaitBar", "PGTop"
    ]
    for panda_node in panda_nodes:
        tag = '+{}'.format(panda_node)
        for nodepath in root.find_all_matches("**/="+tag):
            value_raw = nodepath.get_tag(tag)
            extra_args = read_args(root, value_raw)
            panda_node_class = getattr(panda3d.core, panda_node)
            new_node = panda_node_class(nodepath.name + "_"+panda_node)
            new_nodepath = nodepath.parent.attach_new_node(new_node)
            nodepath.clear_tag(tag)
            nodepath.clear_python_tag(tag)
            for key in nodepath.get_python_tag_keys():
                new_nodepath.set_python_tag(key, nodepath.get_python_tag(key))
            for key in nodepath.get_tag_keys():
                new_nodepath.set_tag(key, nodepath.get_tag(key))
            for child in nodepath.get_children():
                child.reparent_to(new_nodepath)
            nodepath.detach_node()
            tags_as_node_function(root, nodetype=new_node)

def evaluate_property_logic(root):
    tags_as_class(root)
    tags_as_nodepath_function(root)

