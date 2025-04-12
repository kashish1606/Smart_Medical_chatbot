import os
import subprocess
import platform
from gtts import gTTS   # type: ignore
import elevenlabs
from elevenlabs.client import ElevenLabs

# 🔹 Step 1: Load API Key
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
if ELEVENLABS_API_KEY is None:
    raise ValueError("ELEVENLABS_API_KEY environment variable is not set")

# 🔹 Step 2: Text-to-Speech using gTTS
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)

    # Auto-play audio
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'Start-Process -FilePath "{output_filepath}"'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath])
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"Error playing audio: {e}")

# 🔹 Step 3: Text-to-Speech using ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    try:
        # Generate audio
        audio_generator= client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_44100",
            model="eleven_turbo_v2"
        )
        # Convert generator to bytes
        audio_data = b"".join(audio_generator)

        # 🔹 Ensure the MP3 file is saved correctly
        with open(output_filepath, "wb") as f:
            f.write(audio_data)

        print(f"ElevenLabs audio saved to {output_filepath}")

        # 🔹 Convert MP3 to WAV (Required for PowerShell PlaySync)
        wav_filepath = output_filepath.replace(".mp3", ".wav")
        subprocess.run(['ffmpeg', '-i', output_filepath, wav_filepath, '-y'])

        # 🔹 Play the WAV file
        os_name = platform.system()
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', wav_filepath])
            elif os_name == "Windows":  # Windows (Fixed PowerShell command)
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
            elif os_name == "Linux":  # Linux
                subprocess.run(['aplay', wav_filepath])  # Alternative: 'mpg123' or 'ffplay'
            else:
                raise OSError("Unsupported OS")
        except Exception as e:
            print(f"Error playing audio: {e}")

    except Exception as e:
        print(f"Error generating or saving audio: {e}")

# 🔹 Run the function
input_text = "Hi this is AI with Kashish! Auto play testing"
text_to_speech_with_elevenlabs(input_text, output_filepath="C:\\Users\\kashish\\OneDrive\\Desktop\\Python\\final.mp3")
