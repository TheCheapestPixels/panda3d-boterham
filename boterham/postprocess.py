from panda3d.core import CollisionNode, CollisionPolygon
from panda3d.core import GeomVertexReader
from direct.showbase.ShowBase import ShowBase
from .property_logic import evaluate_property_logic


base = ShowBase(windowType='none')


def nodepath_to_collision_polygons(root):
    for nodepath in root.find_all_matches("**/=geom_to_collision_polygon"):
        for c in nodepath.findAllMatches('**/+GeomNode'):
            geomNode = c.node()
            for g in range(geomNode.getNumGeoms()):
                geom = geomNode.getGeom(g).decompose()
                vdata = geom.getVertexData()
                vreader = GeomVertexReader(vdata, 'vertex')
                cChild = CollisionNode('{}'.format(c.getName()))
                for p in range(geom.getNumPrimitives()):
                    prim = geom.getPrimitive(p)
                    for p2 in range(prim.getNumPrimitives()):
                        s = prim.getPrimitiveStart(p2)
                        e = prim.getPrimitiveEnd(p2)
                        v = []
                        for vi in range (s, e):
                            vreader.setRow(prim.getVertex(vi))
                            v.append (vreader.getData3f())
                        colPoly = CollisionPolygon(*v)
                        cChild.addSolid(colPoly)
                c.parent.attachNewNode(cChild)


def postprocess(filename):
    print('post-processing', filename)
    root = loader.load_model(filename)
    evaluate_property_logic(root)
    nodepath_to_collision_polygons(root)
    root.write_bam_file(filename)
