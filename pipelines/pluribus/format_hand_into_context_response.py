def format_hand_into_context_response(hand_stop_on_action, next_action, player):
    context = {
        'variant' : hand_stop_on_action['variant'],
        'ante_trimming_status' : hand_stop_on_action['ante_trimming_status'],
        'hand' : hand_stop_on_action['hand'],
        'players' : [f'p{i}' for i in range(1, len(hand_stop_on_action['players']) + 1)],
        'player' : player,
        'antes' : hand_stop_on_action['antes'],
        'blinds_or_straddles' : hand_stop_on_action['blinds_or_straddles'],
        'min_bet' : hand_stop_on_action['min_bet'],
        'starting_stacks' : hand_stop_on_action['starting_stacks'],
        'actions' : str(hand_stop_on_action['actions']).replace("']", " "),
    }

    return {
        'context' : context,
        'response' : next_action + "'",
    }

