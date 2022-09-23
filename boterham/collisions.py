import panda3d.core


def geom_to_collision_polygons(root, keep=True):
    for c in root.findAllMatches('**/+GeomNode'):
        geomNode = c.node()
        for g in range(geomNode.getNumGeoms()):
            geom = geomNode.getGeom(g).decompose()
            vdata = geom.getVertexData()
            vreader = panda3d.core.GeomVertexReader(vdata, 'vertex')
            cChild = panda3d.core.CollisionNode('{}'.format(c.getName()))
            for p in range(geom.getNumPrimitives()):
                prim = geom.getPrimitive(p)
                for p2 in range(prim.getNumPrimitives()):
                    s = prim.getPrimitiveStart(p2)
                    e = prim.getPrimitiveEnd(p2)
                    v = []
                    for vi in range (s, e):
                        vreader.setRow(prim.getVertex(vi))
                        v.append (vreader.getData3f())
                    colPoly = panda3d.core.CollisionPolygon(*v)
                    cChild.addSolid(colPoly)
            c.parent.attachNewNode(cChild)
            if not keep:
                c.detach_node()

def nodepath_to_collision_polygons(root):
    for nodepath in root.find_all_matches("**/=geom_to_collision_polygon"):
        geom_to_collision_polygons(nodepath)

def set_collision_shapes(nodepath):
    def get_pos_hpr_scale(np):
        return np.get_pos(), np.get_hpr(), np.get_scale()

    def add_shape(nodepath, shape, shape_np):
        nodepath.node().add_solid(shape)
        shape_np.detach_node()

    for shape_np in nodepath.find_all_matches('**/=+CollisionSphere'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.core.CollisionSphere(pos[0], pos[1], pos[2], scale[2])
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+CollisionInvSphere'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.core.CollisionInvSphere(pos[0], pos[1], pos[2], scale[2])
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+CollisionCapsule'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.core.CollisionCapsule(
            pos[0]-(scale[0]/2), pos[1]-(scale[1]/2), pos[2]-(scale[2]/2),
            pos[0]+(scale[0]/2), pos[1]+(scale[1]/2), pos[2]+(scale[2]/2),
            (scale[0]+scale[1])/2
        )
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+CollisionPlane'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.core.CollisionPlane(pos, (0,0,1))
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+CollisionRay'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.core.CollisionRay(*pos, hpr)
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+CollisionLine'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.core.CollisionLine(*pos, hpr)
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+CollisionSegment'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        to_pos = shape.get_pos(shape_np, scale[2])
        shape = panda3d.core.CollisionSegment(pos, to_pos)
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+CollisionBox'):
        pos, hpr, scale = get_pos_hpr_scale(shape_np)
        shape = panda3d.core.CollisionBox(pos, *scale)
        add_shape(nodepath, shape, shape_np)
    for shape_np in nodepath.find_all_matches('**/=+CollisionPolygon'):
        geom_to_collision_polygons(shape_np, keep=False)
        shape_np.show()

def set_collisions(root):
    nodepath_to_collision_polygons(root)
    set_collision_shapes(root)
