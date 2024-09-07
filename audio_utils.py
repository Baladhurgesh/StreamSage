from abc import ABC, abstractmethod
from deepgram import DeepgramClient, SpeakOptions
import os
from dotenv import load_dotenv
import pygame
import requests
import io

load_dotenv()
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
COQUI_LOCAL_URL = os.getenv('COQUI_LOCAL_URL')
PIPER_LOCAL_URL = os.getenv('PIPER_LOCAL_URL')
class SpeechGenerator(ABC):
    @abstractmethod
    def generate_speech(self, text, filename="audio.mp3"):
        pass

    @abstractmethod
    def play_audio(self, filename):
        pass

class DeepGram(SpeechGenerator):
    def __init__(self):
        self.deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    def generate_speech(self, text, filename="audio.mp3"):
        try:
            options = SpeakOptions(
                model="aura-asteria-en",
            )

            text_input = {"text": text}

            response = self.deepgram.speak.v("1").save(filename, text_input, options)
            print(response.to_json(indent=4))
            return filename

        except Exception as e:
            print(f"Exception: {e}")
            return None

    def play_audio(self, filename):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            print("Audio played successfully")
        except Exception as e:
            print(f"Error playing audio: {e}")

class Coqui(SpeechGenerator):
    def __init__(self, url=COQUI_LOCAL_URL):
        self.url = url

    def generate_speech(self, text, filename="audio.mp3"):
        try:
            params = {"text": text}
            response = requests.post(self.url, params=params)

            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Audio saved to {filename}")
                return filename
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None

        except Exception as e:
            print(f"Exception: {e}")
            return None

    def play_audio(self, filename):
        try:
            audio_data = io.BytesIO()
            with open(filename, 'rb') as f:
                audio_data.write(f.read())
            audio_data.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            print("Audio played successfully")
        except Exception as e:
            print(f"Error playing audio: {e}")

class Piper(SpeechGenerator):
    def __init__(self, url=PIPER_LOCAL_URL):
        self.url = url

    def generate_speech(self, text, filename="audio.mp3"):
        try:
            params = {"text": text}
            response = requests.post(self.url, params=params)

            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Audio saved to {filename}")
                return filename
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None

        except Exception as e:
            print(f"Exception: {e}")
            return None

    def play_audio(self, filename):
        try:
            audio_data = io.BytesIO()
            with open(filename, 'rb') as f:
                audio_data.write(f.read())
            audio_data.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            print("Audio played successfully")
        except Exception as e:
            print(f"Error playing audio: {e}")

if __name__ == "__main__":
    sample_text = "What would you like to know?"
    
    # Choose the TTS engine: 'deepgram', 'coqui', or 'piper'
    tts_engine = 'piper'  # You can change this to 'deepgram' or 'piper' to use those engines

    if tts_engine == 'deepgram':
        generator = DeepGram()
    elif tts_engine == 'coqui':
        generator = Coqui()
    elif tts_engine == 'piper':
        generator = Piper()
    else:
        raise ValueError("Invalid TTS engine. Choose 'deepgram', 'coqui', or 'piper'.")

    audio_file = generator.generate_speech(sample_text)
    if audio_file:
        generator.play_audio(audio_file)