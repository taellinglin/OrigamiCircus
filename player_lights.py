# player_lights.py
import math
import random
from panda3d.core import LColor, VBase4, PointLight, Material

def setup_orbiting_lights(player):
    player.lights = []
    # Calculate orbit radius; adjust as needed
    player.light_orbit_radius = 2 * math.sin((player.gamepad_x * player.gamepad_y / 2) + globalClock.get_dt())
    
    for i in range(16):
        light = PointLight(f"light_{i}")
        light_node = player.render.attach_new_node(light)
        light_node.set_pos(0, player.light_orbit_radius * i, 0)

        # Assign a random color from the player's color cycle
        color = random.choice(player.color_cycle)
        light.setColor(color)
        player.render.set_light(light_node)

        # Load the orb model representing the light
        sphere = base.loader.loadModel("orb.bam")
        sphere.reparent_to(light_node)
        sphere.set_color(color)
        
        material = Material()
        material.setEmission(color)
        sphere.setMaterial(material)

        light_properties = {
            "light_node": light_node,
            "sphere": sphere,
            "angle": random.uniform(0, 360),
            "tilt_angle": random.uniform(0, 60),
            "flicker_timer": 0.0,
            "flicker_speed": random.uniform(0.01, 0.05),
            "color_index": random.randrange(0, len(player.color_cycle))
        }
        player.lights.append(light_properties)

def update_lights(player, task):
    # Update each light's flicker, orbit, and color cycling
    for light in player.lights:
        flicker_intensity = random.uniform(0.1, 1)
        current_color = light["sphere"].get_color()
        new_emission_color = VBase4(
            current_color[0] * flicker_intensity,
            current_color[1] * flicker_intensity,
            current_color[2] * flicker_intensity,
            current_color[3]
        )
        light["sphere"].getMaterial().set_emission(new_emission_color)
    
    player_pos = player.actor_rb.get_pos()
    for light_properties in player.lights:
        harmonic_factor = math.sin(task.time * light_properties["angle"] * 0.01)
        light_properties["angle"] += globalClock.get_dt() * 0.05
        x = player_pos.x + player.light_orbit_radius * math.cos(math.radians(light_properties["angle"])) + harmonic_factor * 0.5
        y = player_pos.y + player.light_orbit_radius * math.sin(math.radians(light_properties["angle"])) + harmonic_factor * 0.5
        z_oscillation = math.sin(task.time * 0.5 + light_properties["angle"]) * 0.5
        z = player_pos.z + player.light_orbit_radius * 0.5 * math.sin(math.radians(light_properties["tilt_angle"])) + 0.5 + z_oscillation
        
        light_properties["light_node"].set_pos(x, y, z)
        light_properties["flicker_timer"] += globalClock.get_dt()
        if light_properties["flicker_timer"] >= light_properties["flicker_speed"]:
            light_properties["flicker_timer"] = 0
            light_properties["sphere"].set_scale(random.uniform(1, 2))
        
        light_properties["color_index"] = (light_properties["color_index"] + 1) % len(player.color_cycle)
        color = random.choice(player.color_cycle)
        light_properties["light_node"].set_color(color)
        light_properties["sphere"].set_color(color)
        light_properties["sphere"].getMaterial().set_emission(color)
    
    return task.cont
