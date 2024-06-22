from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def format_hand_into_context_response(hand_stop_on_action, next_action, player, anonymized_hands_dict, no_history, history_max):

    history = [anonymized_hand["actions"] for anonymized_hand in anonymized_hands_dict]
    hands_numbers = [anonymized_hand["hand"] for anonymized_hand in anonymized_hands_dict]
    if history_max is None:
        history_max = len(history)
    history = history[-history_max:] if len(history) > history_max else history
    hands_numbers = hands_numbers[:history_max] if len(hands_numbers) > history_max else hands_numbers
    history_formated = {f"hand {hands_numbers[i]}": history[i] for i in range(len(history)-1)}

    context = {
        'variant' : hand_stop_on_action['variant'],
        'ante_trimming_status' : hand_stop_on_action['ante_trimming_status'],
        'hand' : hand_stop_on_action['hand'],
        'players' : [f'p{i}' for i in range(1, len(hand_stop_on_action['players']) + 1)],
        'player' : player,
        'antes' : hand_stop_on_action['antes'],
        'blinds_or_straddles' : hand_stop_on_action['blinds_or_straddles'],
        'min_bet' : hand_stop_on_action['min_bet'],
        'history' : history_formated,
        'starting_stacks' : hand_stop_on_action['starting_stacks'],
        'actions' : str(hand_stop_on_action['actions']).replace("']", " "),
    }

    if no_history:
        context.pop('history')

    response = next_action + "'"

    tokens_used = len(tokenizer.encode(str(context))) + len(tokenizer.encode(response))

    return {
        'context' : context,
        'response' : response,
    }, tokens_used

