# player.py
from panda3d.core import Vec3, LColor, BitMask32
from direct.actor.Actor import Actor
from direct.task import Task
from panda3d.bullet import BulletRigidBodyNode, BulletCapsuleShape, ZUp
import math
import random

# Import our separated modules
from player_animation import play_animation, tween_to_idle_or_move, update_animation
from player_physics import setup_actor_physics, jump, check_jump_animation, apply_jump_impulse, execute_jump, check_landing
from player_lights import setup_orbiting_lights, update_lights

class Player:
    def __init__(self, render, bullet_world, gamepad_input):
        self.render = render
        self.bullet_world = bullet_world
        self.gamepad_input = gamepad_input

        # Animation-related
        self.actor = None
        self.current_animation = None
        self.override_animation = None

        # Physics-related
        self.actor_rb = None

        # Gamepad input state
        self.gamepad_x = 0.0
        self.gamepad_y = 0.0
        self.mag = 0

        # Lights-related
        self.lights = []
        self.light_orbit_radius = 0
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
        self.color_change_time = 0.001
        self.time_accumulator = 0.0

        # State flags
        self.is_talking = False
        self.is_jumping = False
        self.is_running = False
        self.is_walking = False
        self.is_landing = False
        self.is_falling = False

        self.setup_player()
        setup_orbiting_lights(self)
        taskMgr.add(update_lights, "update_lights", extraArgs=[self], appendTask=True)
        taskMgr.add(check_landing, "landing_check", extraArgs=[self], appendTask=True)
        taskMgr.add(self.update, "player_update")

    def setup_player(self):
        # Load your actor with animations (paths adjusted to your assets)
        self.actor = Actor('witch.bam', {
            'witch_idle': 'witch_idle.bam',
            'witch_walk': 'witch_walk.bam',
            'witch_run': 'witch_run.bam',
            'witch_jump': 'witch_jump.bam',
        })
        self.actor.reparentTo(self.render)
        setup_actor_physics(self)
        play_animation(self.actor, "witch_idle")

    def on_gamepad_move(self, axis, value):
        if axis == 0:
            self.gamepad_x = value
        elif axis == 1:
            self.gamepad_y = value

        self.mag = (self.gamepad_x ** 2 + self.gamepad_y ** 2) ** 0.5
        
        # Only update movement animations if not jumping.
        if not self.is_jumping:
            tween_to_idle_or_move(self)


    def jump(player):
        if player.actor_rb.get_pos().z > 1.0:
            print("Not on the ground, cannot jump")
            return

        jump_impulse_delay = 0.3  
        jump_impulse = Vec3(0, 0, 10)  

        player.actor_rb.getNode(0).set_linear_velocity(Vec3(0, 0, 0))
        player.actor_rb.getNode(0).apply_central_impulse(jump_impulse)
        print(f"Jump initiated: Applied impulse {jump_impulse}")

        from player_animation import play_animation
        play_animation(player.actor, "witch_jump_start", override=True)

        # Set jump-related flags:
        player.is_jumping = True
        player.is_talking = True
        player.is_on_ground = False  # Ensure on-ground is false when jumping

        taskMgr.add(lambda task: check_jump_animation(player, task), "check_jump_animation")
        taskMgr.doMethodLater(jump_impulse_delay, lambda task: apply_jump_impulse(player, task), "jump_impulse_task")

    def update(self, task):
        # Update position based on gamepad input
        move_speed = 0.1  # Adjust as needed
        current_pos = self.actor_rb.get_pos()
        new_pos = current_pos + Vec3(self.gamepad_x * move_speed,
                                    self.gamepad_y * move_speed,
                                    0)
        self.actor_rb.set_pos(new_pos)

        # Rotate the witch based on analog stick input
        if self.mag > 0.01:
            angle = math.degrees(math.atan2(self.gamepad_x, -self.gamepad_y))
            self.actor_rb.set_h(angle)

        # Update state flags based on movement magnitude
        if self.mag > 0.5:
            self.is_running = True
            self.is_walking = False
        elif self.mag > 0.01:
            self.is_running = False
            self.is_walking = True
        else:
            self.is_running = False
            self.is_walking = False

        # Only update movement animations if not jumping.
        if not self.is_jumping:
            tween_to_idle_or_move(self)
        
        return task.cont
