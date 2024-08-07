import os
import subprocess


def convert_wav_to_aiff(input_dir, output_dir):
    """
    Convert WAV files to AIFF format.

    TODO: finish the method. IT needs to also detect the bit rate

    :param input_dir: Path to the directory containing WAV files.
    :param output_dir: Path to the directory where AIFF files will be saved.
    :return: None
    """
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.wav'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.aiff')
            ffmpeg_command = ['ffmpeg', '-i', input_path, output_path]

            subprocess.run(ffmpeg_command, check=True)
            print(f"Converted {filename} to AIFF")
