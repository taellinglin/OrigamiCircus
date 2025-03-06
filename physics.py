# physics.py
from panda3d.bullet import BulletWorld
from panda3d.core import Vec3

class Physics:
    def __init__(self, render):
        self.render = render
        self.bullet_world = BulletWorld()

    def get_bullet_world(self):
        return self.bullet_world

    def step_physics(self, dt):
        # Update physics world with the time step
        self.bullet_world.doPhysics(dt)
