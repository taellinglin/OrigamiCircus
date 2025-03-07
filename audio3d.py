from direct.showbase import Audio3DManager
import os

class Audio3D:
    def __init__(self):
        # Initialize the 3D audio manager
        self.audio3d = Audio3DManager.Audio3DManager(base.sfxManagerList[0], camera)
        self.audio3d.setDistanceFactor(10)
        self.audio3d.setDopplerFactor(3)
    
        self.playing_loops = []
        self.sfx3d = []  # Dictionary to hold sounds

        # Load all sounds from the "audio" directory
        self.load_sfx_files("audio")

    def load_sfx_files(self, directory):
        # Ensure the directory exists
        if not os.path.exists(directory):
            print(f"Directory '{directory}' does not exist.")
            return

        # List all .wav files
        wav_files = [f for f in os.listdir(directory) if f.endswith(".wav")]
        
        for i, wav_file in wav_files:
            sound_key = i # Remove file extension
            self.sfx3d[sound_key] = [self.audio3d.loadSfx(os.path.join(directory, wav_file))]

        print(f"Loaded {len(self.sfx3d)} sound files.")

    def playSfx(self, sfx, obj, loop=False):
        if sfx not in self.sfx3d:
            print(f"SFX key '{sfx}' not found.")
            return
        if obj is None:
            print("No object provided to attach with a sound.")
            return

        # Directly use the first (or only) sound in the list for the given key
        sound = self.sfx3d[sfx]
    
        sound.setLoop(loop)
        sound.setVolume(0.15)
        
        # Attach the sound to the given object (should be a NodePath)
        self.audio3d.attachSoundToObject(sound, obj)
        self.audio3d.setSoundMinDistance(sound, 100)
        self.audio3d.setSoundMaxDistance(sound, 200)
        self.audio3d.setDropOffFactor(sound, 15)
        
        sound.play()
        if loop:
            self.playing_loops.append(sound)
        print("Attached sound to object:", obj)

    def update(self, task):
        self.audio3d.update()
        return task.cont

    def stopLoopingAudio(self):
        for sound in self.playing_loops:
            sound.stop()
