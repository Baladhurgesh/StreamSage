from TTS.api import TTS
import torch
import time
from fastapi import FastAPI
import asyncio
import uvicorn

app = FastAPI()

class CoquiTTS:
    def __init__(self):
        self.tts = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    async def load_model(self):
        start_time = time.time()
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
        self.tts.to(self.device)
        model_load_time = time.time() - start_time
        print(f"Model loading time: {model_load_time:.2f} seconds")

        # Set inference parameters for faster generation
        self.tts.synthesizer.tts_model.inference_padding = 0
        self.tts.synthesizer.tts_model.length_scale = 0.9  # Slightly faster speech
        self.tts.synthesizer.tts_model.use_griffin_lim = True  # Faster but lower quality vocoder

    async def generate_speech(self, text: str, output_file: str = "coqui.wav"):
        if not self.tts:
            await self.load_model()

        start_time = time.time()
        with torch.no_grad():  # Disable gradient calculation for faster inference
            self.tts.tts_to_file(text=text, file_path=output_file)

        inference_time = time.time() - start_time
        print(f"Inference time: {inference_time:.2f} seconds")
        return output_file

coqui_tts = CoquiTTS()

@app.on_event("startup")
async def startup_event():
    await coqui_tts.load_model()

@app.post("/generate_speech")
async def generate_speech_endpoint(text: str, output_file: str = "coqui.wav"):
    result = await coqui_tts.generate_speech(text, output_file)
    return {"message": "Speech generated successfully", "file": result}

if __name__ == "__main__":
    uvicorn.run(app, host="172.20.252.102", port=7777)
    # To run this FastAPI script:
    # 1. Make sure you have all required dependencies installed (FastAPI, uvicorn, TTS, torch)
    # 2. Open a terminal and navigate to the directory containing this script
    # 3. Run the following command:
    #    python coqui_2_tts.py
    # 4. The server will start and listen on http://192.168.1.185:7777
    # 5. You can then make POST requests to http://192.168.1.185:7777/generate_speech
    #    with JSON body containing "text" and optionally "output_file" parameters
    # Example using curl:
    # curl -X POST "http://192.168.1.185:7777/generate_speech" -H "Content-Type: application/json" -d '{"text":"Hello, world!", "output_file":"output.wav"}'
