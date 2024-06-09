from util.loudness import normalize_audio_files

if __name__ == "__main__":
    input_dir = input("Enter the path to your audio files directory: ").strip()
    output_dir = input("Enter the path to your output directory: ").strip()
    target_level = float(input("Enter the target peak level in dB (e.g., -3.0): ").strip())

    normalize_audio_files(input_dir, output_dir, target_level)
