import os
from panda3d.core import AudioSound
from direct.showbase.Audio3DManager import Audio3DManager
class audio3d:
    def __init__(self, base, camera, sfx3d, player):
        # Initializing the 3D audio manager
        self.audio3d = Audio3DManager(base.sfxManagerList[0], camera)
        self.player = player
        self.sfx3d = sfx3d  # A list of sound files
        self.audio3d.setDistanceFactor(1000)
        self.audio3d.setDopplerFactor(300)
        self.playing_loops = []

        # Load all .wav files from the 'audio' directory
        audio_files = sorted([f"audio/{f}" for f in os.listdir("audio") if f.endswith(".wav")])
        
        # Populate the sfx3d dictionary with the loaded sounds
        self.sfx3d_audio = {
            os.path.splitext(f)[0]: base.loader.loadSfx(f"audio/{f}") for f in audio_files
        }

    def enter(self):
        base.task_mgr.add(self.update, "update")

    def playSfx(self, sfx=None, obj=None, loop=False, frequency=None):
        if sfx is None or obj is None:
            print("Sound effect or object not provided.")
            return

        if sfx not in self.sfx3d_audio:
            print("Sound effect not found in sfx3d_audio.")
            return

        sfx3d = self.sfx3d_audio[sfx]

        # If the sound is already playing, skip
        if sfx3d.status() == sfx3d.PLAYING:
            print(f"Sound {sfx3d} is already playing. Skipping.")
            return

        print(f"Playing sound: {sfx3d}")

        # Set the loop on the AudioSound itself
        sfx3d.setLoop(loop)

        # Apply frequency-based play rate adjustment
        if frequency is not None:
            play_rate = frequency / 440.0  # Using 440Hz (A4) as a reference pitch
            sfx3d.setPlayRate(play_rate)

        # Attach the sound to the object in the 3D world
        self.audio3d.attachSoundToObject(sfx3d, obj)
        self.audio3d.setSoundMinDistance(sfx3d, 1)
        self.audio3d.setSoundMaxDistance(sfx3d, 100)
        self.audio3d.setDropOffFactor(50)

        # Play the sound
        sfx3d.play()

        # Keep track of looping sounds for updating their positions
        if loop:
            self.playing_loops.append((sfx3d, obj))

    def updateSoundPosition(self, sound, obj):
        if sound and obj and hasattr(obj, 'get_pos'):
            obj_pos = obj.get_pos()
            # Assuming velocity is zero for stationary objects
            obj_vel = Vec3(0, 0, 0)
            sound.set3dAttributes(obj_pos[0], obj_pos[1], obj_pos[2], obj_vel[0], obj_vel[1], obj_vel[2])
            print(f"Updated sound position to: {obj_pos}")
        else:
            print("Invalid sound or object.")

    def update(self, task):
        # Update the 3D audio system
        self.audio3d.update()

        # Update the position of the sounds attached to objects
        for sound, obj in self.playing_loops:
            if sound and obj:
                if hasattr(obj, 'get_pos'):
                    obj_pos = obj.get_pos()
                    # Assuming velocity is zero for stationary objects
                    obj_vel = Vec3(0, 0, 0)
                    sound.set3dAttributes(obj_pos[0], obj_pos[1], obj_pos[2], obj_vel[0], obj_vel[1], obj_vel[2])
                    print(f"Updated sound position to: {obj_pos}")
                else:
                    print("The object does not have a valid position (get_pos).")
            else:
                print("Sound or object is invalid.")

        return task.cont
