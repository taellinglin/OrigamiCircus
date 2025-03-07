from direct.showbase.ShowBase import ShowBase
from player import Player
from controls import Controls
from world import World
from camera import Camera
from lighting import Lighting
from physics import Physics
from audio3d import Audio3D
import random
from sfx import SoundEmitter
from bgm import BGM
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
        #self.audio3d = Audio3D()
        self.bgm = BGM(1)
        # Ensure portal_sounds is a list (instead of set)
        #self.portal_sounds = list(self.audio3d.sfx3d["portal_loop"])  # Assuming it's a set, convert it to a list

        # Set up sound emitters for lights, attaching a sound to each light
        self.light_sounds = []  # List to hold the sound emitters for the lights
        transient_sfx = base.loader.load_sfx("music/transient.wav")

        self.bgm.playMusic("transient")

        # Create a sound emitter for each light and attach it to the light's position
        #for i, light_properties in enumerate(self.player.lights):  # Use enumerate() for indexing
            # Pick a random sound from available sfx3d keys
            #selected_sfx = random.choice(list(self.audio3d.sfx3d[i]))  

            # Debugging: Print to confirm selection
            #print(f"Selected sound for light {i}: {selected_sfx}")

            # Play the selected sound for the light's sphere
            #self.audio3d.playSfx(sfx=selected_sfx, obj=light_properties["sphere"], loop=True)
            # Add sound emitter to the list
            #self.light_sounds.append(sound_emitter)

        # Add update task to step physics and update camera
        self.taskMgr.add(self.update, "update")
        self.taskMgr.add(self.controls.update, "controls-update")

    def update(self, task):
        # Step physics and update game state
        self.physics.step_physics(globalClock.get_dt())
        self.camera.update_camera(task)
        self.player.update(task)

        # Update sounds for the lights
        for light, sound_emitter in zip(self.player.lights, self.light_sounds):
            # Update the sound position to match the light's position
            light_pos = light["sphere"].get_pos(self.render)
            #sound_emitter.light_node.setPos(light_pos)

            # Debug: Print the position of the light and the sound emitter
            print(f"Light position: {light_pos}, Sound emitter position: {sound_emitter.light_node.getPos()}")

            #sound_emitter.update_sound()

        return task.cont


# Run the app
app = AnimationApp()
app.run()
