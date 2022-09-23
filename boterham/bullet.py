from panda3d.core import TransformState
import panda3d.bullet


def geom_to_bullet_polygons(root, convex=False, keep=True):
    for c in root.findAllMatches('**/+GeomNode'):
        geomNode = c.node()
        # TODO: think of a better way to name dynamic property
        dynamic = bool(root.find_tag("**/=_dynamic"))
        for g in range(geomNode.getNumGeoms()):
            if convex:
                shape = panda3d.bullet.BulletConvexHullShape()
                shape.add_geom(geom)
            else:
                mesh = panda3d.bullet.BulletTriangleMesh()
                mesh.add_geom(geomNode.getGeom(g))
                shape = panda3d.bullet.BulletTriangleMeshShape(mesh, dynamic)
            pos, hpr = g.get_pos(), g.get_hpr()
            root.node().add_shape(shape, TransformState.make_pos_hpr(pos, hpr))
        if not keep:
            c.detach_node()

def nodepath_to_bullet_polygons(root):
    for nodepath in root.find_all_matches("**/=geom_to_bullet_polygon"):
        geom_to_bullet_polygons(nodepath)

def set_bullet_shapes(nodepath):
    def get_pos_hpr_scale(np):
        return np.get_pos(), np.get_hpr(), np.get_scale()

    def add_shape(nodepath, shape, shape_np, pos=(0,0,0), hpr=(0,0,0)):
        nodepath.node().add_shape(shape, TransformState.make_pos_hpr(pos, hpr))
        shape_np.detach_node()

    for shape_np in nodepath.find_all_matches('**/=+BulletSphereShape'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.bullet.BulletSphereShape(scale[2])
        add_shape(nodepath, shape, shape_np, pos, hpr)
    for shape_np in nodepath.find_all_matches('**/=+BulletCapsuleShape'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        radius, height = (scale[0]+scale[1])/2, scale[2]
        shape = panda3d.bullet.BulletCapsuleShape(radius, height, panda3d.bullet.zUp)
        add_shape(nodepath, shape, shape_np, pos, hpr)
    for shape_np in nodepath.find_all_matches('**/=+BulletPlaneShape'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        quat = LQuaternion(); normal.set_hpr(hpr)
        shape = panda3d.bullet.BulletPlaneShape(quat.get_up(), 0)
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+BulletBoxShape'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.bullet.BulletBoxShape(scale)
        add_shape(nodepath, shape, shape_np, pos, hpr)
    for shape_np in nodepath.find_all_matches('**/=+BulletCylinderShape'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        radius, height = (scale[0]+scale[1])/2, scale[2]
        shape = panda3d.bullet.BulletCylinderShape(radius, height, panda3d.bullet.zUp)
        add_shape(nodepath, shape, shape_np, pos, hpr)
    for shape_np in nodepath.find_all_matches('**/=+BulletCylinderShape'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        radius, height = (scale[0]+scale[1])/2, scale[2]
        shape = panda3d.bullet.BulletConeShape(radius, height, panda3d.bullet.zUp)
        add_shape(nodepath, shape, shape_np, pos, hpr)
    for shape_np in nodepath.find_all_matches('**/=+BulletConvexHullShape'):
        geom_to_bullet_polygons(shape_np, convex=True, keep=False)
        shape_np.show()
    for shape_np in nodepath.find_all_matches('**/=+BulletTriangleMeshShape'):
        geom_to_bullet_polygons(shape_np, convex=False, keep=False)
        shape_np.show()
    for shape_np in nodepath.find_all_matches('**/=+BulletTriangleMesh'):
        geom_to_bullet_polygons(shape_np, convex=False, keep=False)
        shape_np.show()

def set_bullet(root):
    nodepath_to_bullet_polygons(root)
    #set_bullet_shapes(root, "BulletBodyNode")
