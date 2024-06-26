from transformers import AutoModelForCausalLM, AutoTokenizer
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2nvtop"
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Use CUDA if available
from pipelines.poker_dataset.format_dataset_to_struct import format_dataset_to_struct
from pipelines.poker_dataset.struct_to_format_llm import struct_to_format_llm

# Définir l'appareil (GPU ou CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Variables globales pour le modèle et le tokenizer
model = None
tokenizer = None

def load_model(settings):
    global model, tokenizer
    model_path = settings["model_path"]
    model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

def get_model():
    global model, tokenizer
    if model is None or tokenizer is None:
        load_model()
    return model, tokenizer


def llm_infer(hand_input, settings):
    """
    Perform inference with LLM model
    """
    model_path = settings["model_path"]
    format = settings["format"]

    # Load model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Format input to match model requirements
    hand_struct = hand_input
    hand_format = struct_to_format_llm(hand_struct)

    # Tokenize input
    input_ids = tokenizer.encode(hand_format, return_tensors="pt").to(device)

    # Generate text
    max_length = 1000
    num_return_sequences = 1
    output = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )

    # Decode output
    output_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return output_text