from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from schemas.hand_format import PokerGame
from services.inference import llm_infer
import os
from mistralai import Mistral

mistral_api_key = os.getenv("MISTRAL_API_KEY")
mistral_job_id = os.getenv("MISTRAL_JOB_ID")

app = FastAPI()

print(f"API key is: {mistral_api_key}")
print(f"Job ID is: {mistral_job_id}")

client = Mistral(api_key=mistral_api_key)
job = client.fine_tuning.jobs.get(job_id = mistral_job_id)

SETTINGS = {
    "client": client,
    "job": job
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend for LLM inference!"}

@app.post("/predict")
def predict(hand_input: PokerGame):
    print(hand_input)
    try:
        result = llm_infer(hand_input, SETTINGS)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/predict_test")
def predict(hand_input: PokerGame):
    print(hand_input)
    try:
        result, hand_format_llm = hand_input
        return {"response": result,
                "input": hand_format_llm}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

