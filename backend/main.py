from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from services.inference import llm_infer

app = FastAPI()

SETTINGS = {
    "model_path": "/home/avakili/finetuning/output/outpok1/final_output",
    "format" : "poker_dataset_v1",
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend for LLM inference!"}

@app.get("/predict")
def predict(hand_input: str):
    try:
        result = llm_infer(hand_input, SETTINGS)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
