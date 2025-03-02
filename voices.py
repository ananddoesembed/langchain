
from typing import List, Dict, Any
import edge_tts
import asyncio
import json
import os
import tempfile
import subprocess


# Function to get all available voices
async def get_voices() -> List[Dict[str, Any]]:
    """Fetch all available English voices from Edge TTS."""
    voices = await edge_tts.list_voices()
    # Filter to only include English voices
    en_voices = [v for v in voices if v["Locale"].startswith("en")]
    return en_voices

def gen_voices():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    generated_voices = loop.run_until_complete(get_voices())

    # Create voice options
    voice_options = [(f"{v['ShortName']}", v['ShortName']) for v in generated_voices]
    return voice_options


# Process input text as list of strings
def process_input_text(text_input):
    """Convert input text to a list of strings."""
    if not text_input.strip():
        return []

    # Try to parse as JSON if it starts with '[' and ends with ']'
    if text_input.strip().startswith('[') and text_input.strip().endswith(']'):
        try:
            return json.loads(text_input)
        except json.JSONDecodeError:
            # If JSON parsing fails, fall back to line splitting
            pass

    # Split by lines
    return [line.strip() for line in text_input.split('\n') if line.strip()]


# Function to convert a list of strings to speech
async def read_string_list(
        text_list: List[str],
        voice: str,
        pause_seconds: float = 1.0
) -> tuple:
    """Read a list of strings with the specified voice."""
    if not text_list or not any(text.strip() for text in text_list):
        return None, "Please enter at least one string to read."

    # Create temporary directory for audio files
    temp_dir = tempfile.mkdtemp()
    audio_files = []

    try:
        # Process each text item
        for i, text in enumerate(text_list):
            if not text.strip():
                continue

            # Generate speech for this item
            file_path = os.path.join(temp_dir, f"item_{i}.mp3")

            # Convert to speech
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(file_path)
            audio_files.append(file_path)

        if not audio_files:
            return None, "No valid text to convert to speech."

        # Combine audio files with silence between them
        combined_file = os.path.join(temp_dir, "combined.mp3")

        # Try to use ffmpeg if available, otherwise just return the first file
        try:

            # Create a file list for ffmpeg
            concat_file = os.path.join(temp_dir, "concat.txt")
            with open(concat_file, "w") as f:
                for i, temp_file in enumerate(audio_files):
                    f.write(f"file '{temp_file}'\n")
                    # Add silence between files (except after the last one)
                    if i < len(audio_files) - 1 and pause_seconds > 0:
                        silence_file = os.path.join(temp_dir, f"silence_{i}.mp3")
                        # Generate silence using ffmpeg
                        subprocess.run([
                            "ffmpeg", "-f", "lavfi", "-i", f"anullsrc=r=24000:cl=mono",
                            "-t", str(pause_seconds), silence_file
                        ], check=True, capture_output=True)
                        f.write(f"file '{silence_file}'\n")

            # Combine files
            subprocess.run([
                "ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_file,
                "-c", "copy", combined_file
            ], check=True, capture_output=True)

            return combined_file, f"Generated speech for {len(audio_files)} items using {voice}."

        except (ImportError, subprocess.SubprocessError) as e:
            # If ffmpeg fails or isn't available, just return the first file
            return audio_files[0], f"Generated speech (without pauses) using {voice}."

    except Exception as e:
        return None, f"Error: {str(e)}"

def read_text_list(text_input, voice, pause_seconds = 0.2):
    # Convert input to list of strings
    text_list = process_input_text(text_input)

    if not text_list:
        return None, "Please enter at least one string to read."

    # Read the strings
    audio_path, message = asyncio.run(read_string_list(
        text_list,
        voice,
        float(pause_seconds)
    ))

    return audio_path, message