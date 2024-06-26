from pipelines.poker_dataset.struct_to_format_llm import struct_to_format_llm
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def llm_infer(hand_input, settings):
    """
    Perform inference with Mistral API
    """

    mistral_api_key = settings["mistral_api_key"]
    mistral_job_id = settings["mistral_job_id"]

    client = MistralClient(api_key=mistral_api_key)

    # Format input to match API requirements
    hand_struct = hand_input.dict()
    print("hello")
    player = hand_struct["player"]
    print(f"Player: {player}")
    
    try :
        hand_format = struct_to_format_llm(hand_struct)
    except Exception as e:
        print(e)
        return str(e)
    print(f"Hand format: {hand_format}")

    job = client.jobs.retrieve(mistral_job_id)
    print(f"Job: {job}")

    chat_response = client.chat(
        model=job.fine_tuned_model,
        messages=[ChatMessage(role="user", content=hand_format)],
    )
    print(f"Chat response: {chat_response}")

    return chat_response.messages[0].content


