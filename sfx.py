from panda3d.core import Filename
from direct.showbase import Audio3DManager
from random import shuffle
import os

class SoundEmitter:
    def __init__(self, render, light_node, sound_file):
        self.render = render
        self.light_node = light_node
        
        # Ensure that the sound file is a string path
        if isinstance(sound_file, str):
            self.sound_file = sound_file
        else:
            raise ValueError("sound_file must be a string representing the path to the sound file.")

        # Initialize the audio3d manager
        self.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
        self.sfx3d = {}

        # Load sound file into the audio3d system
        self.sfx3d["sound"] = [
            self.audio3d.loadSfx(os.path.join("audio", self.sound_file))
        ]
        self.audio3d.setDistanceFactor(10)
        self.audio3d.setDopplerFactor(3)

        # Initialize a list to store currently playing loops
        self.playing_loops = []

        self.create_sound()

    def create_sound(self):
        # Make sure the sound exists in the dictionary
        if "sound" in self.sfx3d:
            sound = self.sfx3d["sound"][0]
            
            # Set loop and volume
            sound.setLoop(True)
            sound.setVolume(1.0)

            # Attach the sound to the light node
            self.audio3d.attachSoundToObject(sound, self.light_node)
            self.audio3d.setSoundMinDistance(sound, 100)
            self.audio3d.setSoundMaxDistance(sound, 200)
            self.audio3d.setDropOffFactor(sound, 15)

            # Play the sound
            sound.play()

            # Save it to the playing loops list if it's looping
            self.playing_loops.append(sound)

            print(f"Sound attached to light node: {str(self.light_node)}")

    def update_sound(self):
        # Update the sound's position based on the light node's position in global space
        if self.light_node:
            light_pos = self.light_node.get_pos(self.render)  # Get the light's position in global space
            self.audio3d.setListenerPosition(light_pos)
            print(f"Updated sound position: {light_pos}")

    def stopLoopingAudio(self):
        for sfx in self.playing_loops:
            sfx.stop()
        self.playing_loops.clear()
        print("Stopped all looping sounds.")
