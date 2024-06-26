from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from schemas.hand_format import PokerGame
from dotenv import load_dotenv
from services.inference import llm_infer
import os

app = FastAPI()

load_dotenv()
SETTINGS = {
    "mistral_api_key": os.getenv("MISTRAL_API_KEY"),
    'mistral_job_id': os.getenv("MISTRAL_JOB_ID"),
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend for LLM inference!"}

@app.post("/predict")
def predict(hand_input: PokerGame):
    print(hand_input)
    try:
        result = llm_infer(hand_input, SETTINGS)
        return {"response mistral": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
