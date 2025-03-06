import os
import subprocess

def convert_blend_files():
    cwd = os.getcwd()
    blend_files = [f for f in os.listdir(cwd) if f.endswith('.blend')]
    
    for blend_file in blend_files:
        bam_file = os.path.splitext(blend_file)[0] + ".bam"
        command = [
            "python", "-m", "blend2bam",
            "--material", "pbr",
            "--textures", "copy",
            "--animations", "embed",
            blend_file, bam_file
        ]
        
        print(f"Converting {blend_file} to {bam_file}...")
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully converted {blend_file} to {bam_file}")
        else:
            print(f"Error converting {blend_file}: {result.stderr}")

if __name__ == "__main__":
    convert_blend_files()
