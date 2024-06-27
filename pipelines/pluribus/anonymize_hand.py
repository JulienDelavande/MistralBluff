def anonymize_hand(hand, player):
    hand = hand.copy()
    hand_actions = hand['actions'][:]
    new_actions = []
    for action in hand_actions:
        if not player in action and 'd dh' in action and 'p' in action:
            new_action = action.split(' ')
            new_action[-1] = '****'
            new_action = ' '.join(new_action)
            new_actions.append(new_action)
        else:
            new_actions.append(action)
            
    hand['actions'] = new_actions
    return hand