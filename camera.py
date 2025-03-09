from panda3d.core import Point3, BitMask32

class Camera:
    def __init__(self, render, player):
        self.render = render
        self.player = player
        self.camera_pivot = self.render.attach_new_node("camera_pivot")
        self.setup_camera()

    def setup_camera(self):
        base.camera.reparent_to(self.camera_pivot)
        base.camera.set_pos(0, -5, 3)
        base.camera.look_at(0, 0, 1)


    def update_camera(self, task):
        actor_pos = self.player.actor_rb.get_pos()
        self.camera_pivot.set_pos(actor_pos)


        return task.cont
