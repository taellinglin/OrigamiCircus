# player.py
from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletCapsuleShape, ZUp
from direct.actor.Actor import Actor
import math

from panda3d.core import Vec3, LColor
import math

class Player:
    def __init__(self, render, bullet_world, gamepad_input):
        self.actor = None
        self.actor_rb = None
        self.gamepad_x = 0.0
        self.gamepad_y = 0.0
        self.gamepad_input = gamepad_input
        self.mag = 0
        self.current_animation = None
        self.override_animation = None
        self.render = render
        self.bullet_world = bullet_world
        self.color_cycle = [
            LColor(1, 0, 0, 1),    # Red
            LColor(1, 0.5, 0, 1),  # Orange
            LColor(1, 1, 0, 1),    # Yellow
            LColor(0, 1, 0, 1),    # Green
            LColor(0, 0, 1, 1),    # Blue
            LColor(0.5, 0, 1, 1),  # Indigo
            LColor(1, 0, 1, 1)     # Violet
        ]
        self.color_index = 0
        self.color_change_time = 0.5  # Time (in seconds) to change color
        self.time_accumulator = 0.0
        self.setup_player()

    def setup_player(self):
        # Load actor
        self.actor = Actor('witch.bam', {
            'witch_idle': 'witch_idle.bam',
            'witch_walk': 'witch_walk.bam',
            'witch_run': 'witch_run.bam',
            'witch_talk': 'witch_talk.bam',
        })

        # Set up player physics
        self.setup_actor_physics()
        self.play_animation('witch_idle')

    def setup_actor_physics(self):
        shape = BulletCapsuleShape(0.5, 1.0, ZUp)
        body_node = BulletRigidBodyNode('Actor')
        body_node.setMass(1.0)
        body_node.addShape(shape)
        self.actor_rb = self.render.attach_new_node(body_node)
        self.actor.reparent_to(self.actor_rb)
        self.bullet_world.attachRigidBody(body_node)
        self.actor_rb.set_pos(0, 0, 0)

    def play_animation(self, anim_name=None, duration=None):
        if anim_name:
            self.override_animation = anim_name
            self.current_animation = anim_name
            self.actor.stop()
            self.actor.loop(anim_name)
            return
        # Handle default animation switching based on joystick magnitude
        mag = self.mag
        deadzone = 0.01
        if mag < deadzone:
            target_animation = "witch_idle"
        elif mag >= deadzone and mag < 0.5:
            target_animation = "witch_walk"
        else:
            target_animation = "witch_run"

        if self.current_animation == target_animation:
            return

        self.current_animation = target_animation
        self.actor.stop()
        if target_animation == "witch_walk":
            self.actor.loop("witch_walk")
        elif target_animation == "witch_run":
            self.actor.loop("witch_run")
        else:
            self.actor.loop("witch_idle")

    def on_gamepad_move(self, axis, value):
        if axis == 0:
            self.gamepad_x = value
        elif axis == 1:
            self.gamepad_y = value

        self.mag = math.sqrt(self.gamepad_x ** 2 + self.gamepad_y ** 2)
        self.play_animation()

    def update(self, task):
        # Handle movement and rotation based on gamepad input
        move_speed = 0.1
        current_pos = self.actor_rb.get_pos()
        new_pos = current_pos + Vec3(self.gamepad_x * move_speed, self.gamepad_y * move_speed, 0)
        self.actor_rb.set_pos(new_pos)

        # Rotate the player based on movement direction
        if self.mag > 0.01:
            angle = math.degrees(math.atan2(self.gamepad_x, -self.gamepad_y))
            self.actor_rb.set_h(angle)
        # Update color cycling
        self.time_accumulator += globalClock.get_dt()
        if self.time_accumulator >= self.color_change_time:
            self.time_accumulator -= self.color_change_time
            self.color_index = (self.color_index + 1) % len(self.color_cycle)
        witch_node = self.actor.find("**/witch_mesh")
        if not witch_node.isEmpty():
            witch_node.setColor(self.color_cycle[self.color_index])

        task.cont
