# main.py
from direct.showbase.ShowBase import ShowBase
from player import Player
from controls import Controls
from world import World
from camera import Camera
from lighting import Lighting
from physics import Physics

class AnimationApp(ShowBase):
    def __init__(self):
        super().__init__()

        # Disable mouse and set background color to black
        self.disable_mouse()
        self.set_background_color(0, 0, 0)

        # Set up physics world
        self.physics = Physics(self.render)
        self.bullet_world = self.physics.get_bullet_world()

        # Set up the world, lighting, camera, and player
        self.world = World(self.render, self.bullet_world)
        self.lighting = Lighting(self.render)
        self.player = Player(self.render, self.bullet_world, None)
        self.camera = Camera(self.render, self.player)
        
        # Set up controls
        self.controls = Controls(self.player)

        # Add update task to step physics and update camera
        self.taskMgr.add(self.update, "update")
        self.taskMgr.add(self.controls.update, "controls-update")


    def update(self, task):
        self.physics.step_physics(globalClock.get_dt())
        self.camera.update_camera(task)
        self.player.update(task)
        return task.cont

# Run the app
app = AnimationApp()
app.run()
