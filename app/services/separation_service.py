import os
from app.models.audio_separator import AudioSeparator

def separate_audio(input_filepath: str, output_dir: str) -> dict:
    """
    Orchestrates the call to the Demucs-based model.
    Returns a dict of {stem_name: path_to_stem}.
    """
    # Create a subfolder for outputs
    demucs_output_dir = os.path.join(output_dir, "demucs_output")
    os.makedirs(demucs_output_dir, exist_ok=True)

    # Initialize or retrieve the model
    separator = AudioSeparator()
    stems_paths = separator.separate(input_filepath, demucs_output_dir)

    return stems_paths

