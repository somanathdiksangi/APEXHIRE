# src/tools/speech_tools.py
import os
import json
from openai import OpenAI
from pydub import AudioSegment # For basic audio format conversion if needed

# Initialize the OpenAI client
# It will automatically pick up OPENAI_API_KEY from environment variables
client = OpenAI()

def text_to_speech(text: str, output_filename: str = "interviewer_speech.mp3") -> str:
    """
    Converts a given text into spoken audio using OpenAI's TTS and saves it to a file.

    Args:
        text (str): The text content to be converted to speech.
        output_filename (str): The name of the file to save the audio. Defaults to "interviewer_speech.mp3".

    Returns:
        str: The full path to the generated audio file, or an error message if creation fails.
    """
    try:
        if not os.getenv("OPENAI_API_KEY"):
            return json.dumps({"error": "OPENAI_API_KEY environment variable not set for TTS."}, indent=2)

        # Ensure the output directory exists if output_filename includes a path
        output_dir = os.path.dirname(output_filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # OpenAI TTS supports various voices: 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
        # 'alloy' is often a good default.
        speech_response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )

        full_output_path = os.path.abspath(output_filename)
        speech_response.stream_to_file(full_output_path)
        
        print(f"DEBUG: Text-to-Speech generated: {full_output_path}")
        return json.dumps({"status": "success", "audio_filepath": full_output_path}, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Failed to convert text to speech: {e}"}, indent=2)

def speech_to_text(audio_filepath: str, output_format: str = "mp3") -> str:
    """
    Transcribes spoken audio from a file into text using OpenAI's Whisper API.
    Supports various audio formats (e.g., mp3, mp4, m4a, wav, flac).
    If the input format is not directly supported by Whisper, pydub can attempt conversion.

    Args:
        audio_filepath (str): The path to the audio file containing the spoken response.
        output_format (str): The desired format for potential conversion if input is not optimal. (e.g., "mp3")

    Returns:
        str: The transcribed text, or an error message if transcription fails.
    """
    try:
        if not os.path.exists(audio_filepath):
            return json.dumps({"error": f"Audio file not found at: {audio_filepath}"}, indent=2)
        if not os.getenv("OPENAI_API_KEY"):
            return json.dumps({"error": "OPENAI_API_KEY environment variable not set for STT."}, indent=2)

        # Ensure the file is in a compatible format for Whisper, convert if necessary
        # Whisper API generally handles many formats, but mp3 is widely compatible.
        # If your input audio is consistently in one of Whisper's natively supported formats (mp3, mp4, m4a, wav, flac, webm, aac, ogg),
        # you might not need pydub for simple cases.
        # For robustness, especially if accepting diverse user audio inputs:
        
        # Determine the input format from the file extension
        _, file_extension = os.path.splitext(audio_filepath)
        file_extension = file_extension.lower().lstrip('.')

        processed_audio_path = audio_filepath
        if file_extension not in ['mp3', 'mp4', 'm4a', 'wav', 'flac', 'webm', 'aac', 'ogg']:
            # Attempt to convert using pydub if it's an unsupported format
            try:
                audio = AudioSegment.from_file(audio_filepath, format=file_extension)
                processed_audio_path = f"{os.path.splitext(audio_filepath)[0]}.{output_format}"
                audio.export(processed_audio_path, format=output_format)
                print(f"DEBUG: Converted audio from {file_extension} to {output_format} at {processed_audio_path}")
            except Exception as e:
                return json.dumps({"error": f"Failed to convert audio format using pydub: {e}"}, indent=2)


        with open(processed_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text" # To get plain text directly
            )
        
        print(f"DEBUG: Speech-to-Text transcribed: {transcript[:100]}...")
        return json.dumps({"status": "success", "transcribed_text": transcript}, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Failed to transcribe speech to text: {e}"}, indent=2)