import os
from groq import Groq

# Initialize the Groq client
client = Groq()


filename = os.path.dirname(__file__) + '/extracted_audio.mp3'
with open(filename, "rb") as file:
    # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
      file=(filename, file.read()), # Required audio file
      model="distil-whisper-large-v3-en", # Required model to use for transcription
      prompt="Specify context or spelling",  # Optional
      response_format="json",  # Optional
      language="en",  # Optional
      temperature=0.0  # Optional
    )
    # Print the transcription text
    print(transcription.text)