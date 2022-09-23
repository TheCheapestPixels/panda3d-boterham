import sys
from direct.showbase.ShowBase import ShowBase
from boterham.loader import boterham_load_model, make_bullet_world

base = ShowBase()
boterham_load_model("test.bam").reparent_to(render)
base.accept("escape", sys.exit)
base.cam.set_y(-32)
base.bullet_world = make_bullet_world(render, True)

def update_bullet_world(task):
    base.bullet_world.do_physics(base.clock.dt, 4, 1/ 240.)
    return task.cont
base.task_mgr.add(update_bullet_world)

render.ls()
base.run()
