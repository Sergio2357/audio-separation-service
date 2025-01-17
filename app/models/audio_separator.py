import os
import torch
from demucs.pretrained import get_model
from demucs.apply import apply_model
from demucs.audio import AudioFile
import torchaudio

class AudioSeparator:
    def __init__(self, model_name: str = "htdemucs", device: str = "cpu"):
        """
        Initializes a Demucs model. Defaults to htdemucs on CPU.
        If you have a GPU available in Docker, you can set device='cuda'.
        """
        self.model = get_model(model_name)
        self.model.to(device)
        self.model.eval()
        self.device = device

    def separate(self, input_filepath: str, output_dir: str) -> dict:
        """
        Run Demucs on the input file. Returns {stem_name: path_to_stem.wav}.
        """
        # 1. Read the audio → shape: (channels, length)
        wav = AudioFile(input_filepath).read(
            streams=0,
            samplerate=self.model.samplerate,
            channels=self.model.audio_channels
        )
        wav = wav.to(self.device)

        # 2. Add a batch dimension → shape: (1, channels, length)
        print("Shape before unsqueeze:", wav.shape)
        wav = wav.unsqueeze(0)
        print("Shape after unsqueeze:", wav.shape)

        # 3. Apply the Demucs model → typically shape: (1, n_stems, channels, length)
        sources = apply_model(
            self.model,
            wav,
            device=self.device,
            split=True,
            overlap=0.25
        )

        # 4. Remove the batch dimension → shape: (n_stems, channels, length)
        sources = sources.squeeze(0)
        print(f"Shape after squeeze(0): {sources.shape}")

        # Typically the model sources are ["drums", "bass", "other", "vocals"], etc.
        stem_names = self.model.sources
        stems_paths = {}

        # 5. For each stem: shape: (channels, length)
        for i, stem_name in enumerate(stem_names):
            stem_filename = os.path.join(output_dir, f"{stem_name}.wav")
            audio_tensor = sources[i]  # now (channels, length)

            print(f"Saving stem '{stem_name}' with shape: {audio_tensor.shape}")
            torchaudio.save(
                stem_filename,
                audio_tensor.cpu(),
                sample_rate=self.model.samplerate
            )
            stems_paths[stem_name] = stem_filename

        return stems_paths

