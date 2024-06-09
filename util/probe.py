import subprocess


def get_audio_codec(input_file):
    """

    Get audio codec from input file.

    :param input_file: The path of the input audio file.
    :return: The name of the audio codec as a string.

    """
    # Command to get audio codec information
    command = [
        'ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries',
        'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', input_file
    ]

    # Run the command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result.stdout.strip()
