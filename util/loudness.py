import os
import re
import subprocess

from util.probe import get_audio_codec


def get_peak_level(input_file):
    """
    :param input_file: The input file for which the peak level needs to be determined.
    :return: The peak level value in dB, or None if it cannot be determined.

    This method takes an input file and uses FFmpeg to determine the peak level information.
    It runs the FFmpeg command with the 'volumedetect' filter and captures the output.
    The peak level is extracted from the output using a regular expression match.

    Example usage:
    input_file = 'example.wav'
    peak_level = get_peak_level(input_file)
    print(f"The peak level of {input_file} is {peak_level} dB")
    """
    # Command to get peak level information
    command = [
        'ffmpeg', '-i', input_file, '-af', 'volumedetect', '-f', 'null', '-'
    ]

    # Run the command and capture the output
    result = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
    output = result.stderr

    # Extract the max volume (peak level) value
    peak_match = re.search(r'max_volume:\s*(-?\d+(\.\d+)?)\s*dB', output)
    if peak_match:
        return float(peak_match.group(1))
    else:
        return None


def normalize_audio_files(input_dir, output_dir, target_level=-3.0):
    """
    Normalizes audio files in the input directory and saves them in the output directory.

    :param input_dir: The directory containing the input audio files.
    :param output_dir: The directory to save the normalized audio files.
    :param target_level: The target level in decibels (dB) to normalize the audio files. Default value is -3.0 dB.
    :return: None

    This method loops through all files in the input directory and checks if they have supported audio file
    extensions (.mp3 and .wav). For each supported audio file, it calculates the peak level using the get_peak_level(
    ) function, and determines the gain adjustment needed to normalize the audio file to the target level. It then
    retrieves the audio codec of the input file using the get_audio_codec() function. If the codec is PCM-based,
    it includes the codec arguments for preservation of the original format. Next, it constructs an ffmpeg command to
    normalize the audio file by adjusting the volume with the calculated gain adjustment. Finally, it runs the ffmpeg
    command using subprocess.run() and prints the normalization results.

    Note: The get_peak_level() and get_audio_codec() functions are not included here and should be defined separately
    before calling this method.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Supported audio file extensions
    audio_extensions = ('.mp3', '.wav')

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(audio_extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Get the peak level of the file
            peak_level = get_peak_level(input_path)
            if peak_level is None:
                print(f"Could not determine peak level for {filename}")
                continue

            # Calculate the gain adjustment needed
            gain_adjustment = target_level - peak_level

            # Get the audio codec of the input file to preserve the original format
            codec = get_audio_codec(input_path)
            codec_args = []
            if codec.startswith('pcm'):
                codec_args = ['-c:a', codec]

            # ffmpeg command to normalize the audio file
            ffmpeg_command = [
                'ffmpeg',
                '-i', input_path,
                '-af', f'volume={gain_adjustment}dB',
                '-y',  # Overwrite output file without asking
                *codec_args,
                output_path
            ]

            # Run the ffmpeg command
            subprocess.run(ffmpeg_command, check=True)
            print(f"Normalized {filename} from {peak_level} dB to {target_level} dB")
