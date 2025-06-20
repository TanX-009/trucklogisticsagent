import subprocess
import tempfile
import os
import ffmpeg

WHISPER_DIR = "/home/tanx/C/trucklogisticsagent/backend/whisper.cpp"


def transcribe_audio(file) -> str:
    # Save uploaded file with correct extension
    _, ext = os.path.splitext(file.filename or "")
    ext = ext.lower() if ext else ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_input:
        file.save(temp_input.name)
        temp_input_path = temp_input.name

    # Convert to .wav for whisper.cpp
    print(f"Converting {ext} to wav")
    temp_wav_path = temp_input_path.rsplit(".", 1)[0] + ".wav"
    try:
        (
            ffmpeg.input(temp_input_path)
            .output(temp_wav_path, format="wav", acodec="pcm_s16le", ac=1, ar=16000)
            .run(quiet=True, overwrite_output=True)
        )
    except ffmpeg.Error as e:
        os.remove(temp_input_path)
        raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}")
    print("Conversion complete")

    os.remove(temp_input_path)  # Clean original file
    print(f"Removed: {temp_input_path}")

    # Whisper CLI output path
    output_txt_path = f"{temp_wav_path}.txt"

    print("Transcripting...")
    # Run whisper.cpp
    result = subprocess.run(
        [
            f"{WHISPER_DIR}/build/bin/whisper-cli",
            "-m",
            f"{WHISPER_DIR}/models/ggml-small.en.bin",
            "-f",
            temp_wav_path,
            "-otxt",
        ],
        capture_output=True,
        text=True,
    )
    print("done")

    if result.returncode != 0:
        os.remove(temp_wav_path)
        raise RuntimeError(f"Whisper CLI failed:\n{result.stderr}")

    if not os.path.exists(output_txt_path):
        os.remove(temp_wav_path)
        raise FileNotFoundError(f"Whisper output not found at {output_txt_path}")

    with open(output_txt_path, "r", encoding="utf-8") as f:
        transcript = f.read().strip()
    print(f"Transcript: {transcript}")

    os.remove(temp_wav_path)
    os.remove(output_txt_path)
    return transcript
