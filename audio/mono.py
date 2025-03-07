import os
from pydub import AudioSegment

def convert_stereo_to_mono():
    # Get the current working directory
    directory = os.getcwd()

    # Get all .wav files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            filepath = os.path.join(directory, filename)
            try:
                # Load the stereo .wav file
                audio = AudioSegment.from_wav(filepath)
                
                # Check if the audio is stereo (2 channels)
                if audio.channels == 2:
                    # Convert stereo to mono
                    mono_audio = audio.set_channels(1)
                    
                    # Save the new mono audio with the same filename
                    new_filepath = os.path.join(directory, f"mono_{filename}")
                    mono_audio.export(new_filepath, format="wav")
                    print(f"Converted {filename} to mono.")
                else:
                    print(f"{filename} is already mono, skipping.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Convert all .wav files in the current directory to mono
    convert_stereo_to_mono()
