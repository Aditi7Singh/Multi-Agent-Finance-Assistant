from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import whisper
from gtts import gTTS
import tempfile
import os
from datetime import datetime

app = FastAPI()

# Initialize Whisper model
model = whisper.load_model("base")

class TextToSpeechRequest(BaseModel):
    text: str
    language: str = "en"

class SpeechResult(BaseModel):
    text: str
    confidence: float
    language: str
    timestamp: str

@app.post("/speech-to-text", response_model=SpeechResult)
async def speech_to_text(audio: UploadFile = File(...)):
    try:
        # Save uploaded audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            content = await audio.read()
            temp_audio.write(content)
            temp_audio.flush()

        # Transcribe audio using Whisper
        result = model.transcribe(temp_audio.name)

        # Clean up temporary file
        os.unlink(temp_audio.name)

        return SpeechResult(
            text=result["text"],
            confidence=result.get("confidence", 0.0),
            language=result.get("language", "en"),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        # Create temporary file for audio output
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            # Convert text to speech
            tts = gTTS(text=request.text, lang=request.language)
            tts.save(temp_audio.name)

            # Read the audio file
            with open(temp_audio.name, 'rb') as audio_file:
                audio_content = audio_file.read()

            # Clean up temporary file
            os.unlink(temp_audio.name)

            return audio_content

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}