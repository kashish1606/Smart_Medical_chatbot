#Step 1 (a): Setup text to speech- TTS model with gTTS 
import os
from gtts import gTTS   # type: ignore

def text_to_speech_with_gtts(input_text,output_filepath):
    language="en"
    audioobj=gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

input_text="Hi this is AI with Kashish!"
text_to_speech_with_gtts(input_text=input_text,output_filepath="gtts_testing.mp3")

#Step 1 (b): Setup text to speech- TTS model with elevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs(input_text,output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2",
    )
    elevenlabs.save(audio,output_filepath)
text_to_speech_with_elevenlabs(input_text,output_filepath="elevenlabs_testing.mp3")

#Step 2: Use Model for Text Output to Voice
ELEVENLABS_API_KEY