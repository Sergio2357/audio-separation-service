import requests
from pydub import AudioSegment
import os

def cut_and_send_audio(file_path: str, start_ms: int, end_ms: int, url: str):
    """
    Cut a portion of the audio file from start_ms to end_ms (ms),
    export that snippet as a .wav, and send it to the given endpoint.
    """
    # 1. Load and slice the audio
    snippet = AudioSegment.from_file(file_path)[start_ms:end_ms]

    # 2. Export the sliced snippet to a temporary .wav
    snippet_path = "temp_snippet.wav"
    snippet.export(snippet_path, format="wav")

    # 3. Send the snippet via POST to the endpoint
    with open(snippet_path, "rb") as f:
        response = requests.post(url, files={"file": ("snippet.wav", f, "audio/wav")})

    # 4. Cleanup the temp file
    os.remove(snippet_path)

    return response


def test_cut_and_send():
    """
    Example usage:
    Cut 2-6s portion of 'sample.wav' and send to 'http://localhost:8000/audio/separate'
    """
    audio_file = "George Michael - Careless Whisper.wav"
    endpoint = "http://localhost:8000/audio/separate"  # adjust if different
    resp = cut_and_send_audio(audio_file, 2000, 6000, endpoint)

    print(f"Status code: {resp.status_code}")
    if resp.status_code == 200:
        print("Snippet posted successfully!")
    else:
        print("Something went wrong:", resp.text)


if __name__ == "__main__":
    test_cut_and_send()

