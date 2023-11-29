import os

from elevenlabs import generate, play
from elevenlabs import set_api_key


def speak_tts(self, text: str) -> str:
    """
    Send a voice message to the user using a TTS engine.

    Args:
        text (str): The text to be spoken.

    Returns:
        str: Status of the voice message
    """
    print(f"Running speak_tts with text={text}")
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise Exception(f"User did not provide their TTS API key")
    else:
        set_api_key(api_key)

    try:
        audio = generate(text=text, voice="Adam", model="eleven_monolingual_v1")
        play(audio, use_ffmpeg=False)  # for some reason use_ffmpeg doesn't work for me (I don't hear the audio)
        print(f"TTS played successfully")
        return "Voice message was delivered to the user successfully"
    except Exception as e:
        print(f"TTS failed with: {e}")
        raise e
