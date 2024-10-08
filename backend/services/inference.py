from pipelines.poker_dataset.struct_to_format_llm import struct_to_format_llm

def llm_infer(hand_input, settings):
    """
    Perform inference with Mistral API
    """

    job = settings["job"]
    client = settings["client"]


    # Format input to match API requirements
    hand_struct = hand_input.dict()
    hand_format = struct_to_format_llm(hand_struct)

    print(f"Hand format: {hand_format}")

    chat_response = client.chat.complete(
        model=job.fine_tuned_model,
        messages = [
        {
            "role": "user",
            "content":hand_format,
        },
    ]
    )

    print(f"Chat response: {chat_response}")

    return chat_response.choices[0].message.content, hand_format


