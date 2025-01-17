from pydub import AudioSegment
from pydub.playback import play

def play_audio(file_path: str):
    """
    Cut the audio file between start_ms and end_ms (in milliseconds)
    and play that portion.
    """
    audio = AudioSegment.from_file(file_path)
    play(audio)

def cut_and_play_audio(file_path: str, start_ms: int, end_ms: int):
    """
    Cut the audio file between start_ms and end_ms (in milliseconds)
    and play that portion.
    """
    audio = AudioSegment.from_file(file_path)
    snippet = audio[start_ms:end_ms]
    play(snippet)

def test_cut_and_play():
    """
    Load an audio file, cut it to a specified portion, and play that snippet.
    """
    audio_path = "George Michael - Careless Whisper.wav"  # adjust to your file
    audio_path = "outputs/other.wav"
    # cut_and_play_audio(audio_path, start_ms=2000, end_ms=6000)
    play_audio(audio_path)

if __name__ == "__main__":
    test_cut_and_play()
