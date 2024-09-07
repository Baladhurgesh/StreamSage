from dotenv import load_dotenv
import os
from groq import Groq

from audio_utils import Piper

# Load environment variables from .env file
load_dotenv()

# Print contents of dotenv to see if it's loading properly
# Initialize the Groq client with API key from .env
transcriber = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Initialize the Groq client for chat
chat_client = Groq(api_key=os.getenv('GROQ_API_KEY2'))

# Function to interact with the chat model
        # 4. If the transcription doesn't contain enough information to fully answer the question, acknowledge this and offer the best possible interpretation or suggestion based on what's available.
        # 5. Consider potential visual elements that might not be captured in the transcription but could be relevant to the user's question.
        # 6. Provide your answer in a conversational tone, as if you're a helpful companion watching the video alongside the user.
        # 7. If appropriate, suggest what the user might want to pay attention to next in the video to gain more clarity.
def chat_with_model(context, question, model="llama3-8b-8192"):
    try:
        prompt = f"""
        Context: The following is a transcription from a live video the user is currently watching:
        {context}

        The user is confused and has the following question:
        {question}

        Instructions:
        1. Analyze the provided transcription carefully, keeping in mind it's from a live video the user is watching right now.
        2. Consider the real-time nature of the content and any potential gaps or ambiguities in the transcription.
        3. Address the user's confusion directly, providing a clear and helpful explanation based on the context.

        Do not talk about the video or the user's question. Just provide a response to the user's question briefly.
        """

        response = chat_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant designed to aid users in real-time as they watch live video content. Your goal is to clarify confusions, provide insights, and enhance the viewer's understanding based on transcribed audio from the video."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,  # Slightly increased for more dynamic responses
            max_tokens=4096,
            top_p=0.95,
            stream=False,
            stop=None
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error during chat interaction: {str(e)}")




def transcribe_audio(filename=None):
    if filename is None:
        filename = "/mnt/c/Users/barat/Downloads/recorded_audio.mp3"

    with open(filename, "rb") as file:
        try:
            # Create a transcription of the audio file
            transcription = transcriber.audio.transcriptions.create(
              file=(filename, file.read()), # Required audio file
              model="distil-whisper-large-v3-en", # Required model to use for transcription
              prompt="Specify context or spelling",  # Optional
              response_format="json",  # Optional
              language="en",  # Optional
              temperature=0.0  # Optional
            )
            # Print the transcription text
            print(transcription.text)
            return transcription.text
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")

def main():
    try:
        # Call the transcribe_audio function
        transcription = transcribe_audio()

        # Get user question
        user_question = "What happened from 1943?"

        # Synthesize speech for the user's question
        
        # Initialize Piper TTS engine
        piper = Piper()

        # Generate speech for the user's question
        question_audio_file = piper.generate_speech(user_question, "user_question.wav")

        if question_audio_file:
            print(f"User question audio saved to: {question_audio_file}")
            # Play the generated audio
            piper.play_audio(question_audio_file)
        else:
            print("Failed to generate speech for the user's question.")

        # Call the chat_with_ai function with the transcription and user question
        ai_response = chat_with_model(transcription, user_question)

        # Print the AI's response
        print("\nAI Assistant's Response:")
        print(ai_response)

        answer_audio_file = piper.generate_speech(ai_response, "answer.wav")
        if answer_audio_file:
            print(f"AI answer audio saved to: {answer_audio_file}")
            # Play the generated audio
            piper.play_audio(answer_audio_file)
        else:
            print("Failed to generate speech for the AI's answer.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


    


if __name__ == "__main__":
    main()