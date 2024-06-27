def split_hand_by_actions(hand, player):
    hand = hand.copy()
    hand_actions = hand['actions'][:]
    hands = []
    rest_of_actions = []
    new_actions = []
    for action in hand_actions:
        if player in action and not 'd dh' in action:
            new_action = action.split(' ')
            new_actions.append(new_action[0])
            rest_of_action = ' '.join(new_action[1:])
            rest_of_actions.append(rest_of_action)
            hand_copy = hand.copy()
            hand_copy['actions'] = new_actions.copy()
            hands.append(hand_copy)
            new_actions[-1] = action
        else:
            new_actions.append(action)
        
    return hands, rest_of_actions
