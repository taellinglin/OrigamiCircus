from panda3d.core import Vec3, LColor, PointLight, Material, VBase4
from panda3d.bullet import BulletRigidBodyNode, BulletCapsuleShape, ZUp
from direct.actor.Actor import Actor
import math
import random
from panda3d.core import NodePath

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
        self.color_change_time = 0.001  # Time (in seconds) to change color
        self.time_accumulator = 0.0
        self.setup_player()
        self.setup_orbiting_lights()

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

    def setup_orbiting_lights(self):
        self.lights = []
        self.light_orbit_radius = 2*math.sin((self.gamepad_x*self.gamepad_y/2)+globalClock.get_dt())  # How far the lights orbit the player
        
        for i in range(16):  # Create 7 ROYGBIV lights
            light = PointLight(f"light_{i}")
            light_node = self.render.attach_new_node(light)
            light_node.set_pos(0, self.light_orbit_radius*i, 0)

            # Assign a random color from the ROYGBIV spectrum to the light
            color = random.choice(self.color_cycle)
            light.setColor(color)
            self.render.set_light(light_node)

            # Create the sphere to represent the light
            sphere = base.loader.loadModel("orb.bam")
            sphere.reparent_to(light_node)
            #sphere.set_scale(random.uniform(0.001, 0.01))  # Random scale between 1 and 2
            
            # Set a random color for the orb as well
            sphere.set_color(color)  # Set the color of the sphere to the same color as the light
            # Create a material and set its emission color
            material = Material()
            material.setEmission(color)
            sphere.setMaterial(material)
            # Store light and its properties in a dictionary
            light_properties = {
                "light_node": light_node,
                "sphere": sphere,
                "angle": random.uniform(0, 360),  # Random start angle for the orbit
                "tilt_angle": random.uniform(0, 60),  # Random tilt between 0 and 30 degrees
                "flicker_timer": 0.0,  # Timer to control flicker
                "flicker_speed": random.uniform(0.01, 0.05),  # Speed of flickering
                "color_index": random.randrange(0,len(self.color_cycle))
            }
            
            # Add the light's properties to the list
            self.lights.append(light_properties)

    def update(self, task):
        # Handle movement and rotation based on gamepad input
        move_speed = 0.1
        for light in self.lights:
            # Generate a random flicker intensity factor (could be sinusoidal for smoother flickering)
            flicker_intensity = random.uniform(0.1, 1)  # Random flicker intensity between 0.5 and 1.5

            # Optionally use a sine wave for smoother flickering
            # flicker_intensity = 1 + 0.5 * sin(task.time * 10)  # Oscillates intensity smoothly

            # Set the new emission intensity
            current_color = light["sphere"].get_color()
            new_emission_color = VBase4(
                current_color[0] * flicker_intensity, 
                current_color[1] * flicker_intensity, 
                current_color[2] * flicker_intensity, 
                current_color[3]
            )
            
            light["sphere"].getMaterial().set_emission(new_emission_color)
        
        current_pos = self.actor_rb.get_pos()
        new_pos = current_pos + Vec3(self.gamepad_x * move_speed, self.gamepad_y * move_speed, 0)
        self.actor_rb.set_pos(new_pos)

        for light_properties in self.lights:
            light_properties["angle"] += 0.005  # Increase the angle of each light by
            light_properties["sphere"].set_hpr(light_properties["angle"], light_properties["tilt_angle"], 0)
            # Flicker the light
            light_properties["flicker_timer"] += 0.01

        # Rotate the player based on movement direction
        if self.mag > 0.01:
            angle = math.degrees(math.atan2(self.gamepad_x, -self.gamepad_y))
            self.actor_rb.set_h(angle)

        # Update color cycling for player
        self.time_accumulator += globalClock.get_dt()
        if self.time_accumulator >= self.color_change_time:
            self.time_accumulator -= self.color_change_time
            self.color_index = (self.color_index + 1) % len(self.color_cycle)
        witch_node = self.actor.find("**/witch_mesh")
        if not witch_node.isEmpty():
            witch_node.setColor(self.color_cycle[self.color_index])

        # Update the orbiting lights' positions and flickering
        player_pos = self.actor_rb.get_pos()  # Get the player's current position
        for light_properties in self.lights:
            # Harmonic oscillation on x, y based on light angle and time
            harmonic_factor = math.sin(task.time * light_properties["angle"] * 0.01)  # Harmonic factor with time-based oscillation
            light_properties["angle"] += globalClock.get_dt() * 0.05 # Rotate the lights at a constant speed

            # Apply tilt to the orbit path
            tilt_rad = math.radians(light_properties["tilt_angle"])
            x = player_pos.x + self.light_orbit_radius * math.cos(math.radians(light_properties["angle"])) + harmonic_factor * (0.5)
            y = player_pos.y + self.light_orbit_radius * math.sin(math.radians(light_properties["angle"])) + harmonic_factor * (0.5)
            
            # Oscillation in the Z-direction using a sine wave to create up/down movement
            z_oscillation = math.sin(task.time * (0.5) + light_properties["angle"]) * (0.5)  # Adjust amplitude (0.5) as needed

            z = player_pos.z + self.light_orbit_radius * 0.5 * math.sin(math.radians(light_properties["tilt_angle"])) + (0.5) + z_oscillation  # Tilt effect on the Z-axis

            # Update the position of the light node in the tilted orbit with harmonic oscillation
            light_properties["light_node"].set_pos(x, y, z)

            # Update flickering effect by changing scale of the sphere randomly
            light_properties["flicker_timer"] += globalClock.get_dt()
            if light_properties["flicker_timer"] >= light_properties["flicker_speed"]:
                light_properties["flicker_timer"] = 0
                light_properties["sphere"].set_scale(random.uniform(1, 2))  # Random scale flicker

            # Color cycling for emission (Stepwise)
            # Stepwise cycle through the color cycle
            light_properties["color_index"] = (light_properties["color_index"] + 1) % len(self.color_cycle)
            color = random.choice(self.color_cycle)  # Get the color from the cycle
            light_properties["light_node"].set_color(color)  # Set the light color
            light_properties["sphere"].set_color(color)  # Set the orb color

            # Update the emission color to match the new color
            light_properties["sphere"].getMaterial().set_emission(color)
            
            print(light_properties["sphere"])

        return task.cont
    def get_pos(self, reference=None):
        """Returns the player's position relative to the given reference node."""
        
        # Check if the actor and rigidbody are properly initialized
        if self.actor is None:
            print("Error: Actor is not initialized or is None.")
            return None  # Return None if actor is not initialized
        
        if self.actor_rb is None:
            print("Error: Rigidbody is not initialized or is None.")
            return None  # Return None if rigidbody is not initialized

        # Debug: Print the rigidbody's current position
        print(f"Rigidbody's current position: {self.actor_rb.get_pos()}")
        
        if reference:
            # Check if the reference node is valid
            if isinstance(reference, NodePath):
                print(f"Getting position relative to reference node: {reference.get_name()}")
                return self.actor_rb.get_pos(reference)  # Use rigidbody's position relative to the reference
            else:
                print(f"Warning: Reference provided is not a valid NodePath. Returning global position instead.")
        
        # Return the global position of the rigidbody if no valid reference is provided
        return self.actor_rb.get_pos()  # Get the position from rigidbody instead of actor

