import os
from pathlib import Path

def format_dataset_to_struct(hand_txt, player_name='IlxxxlI'):
    hand_txt = hand_txt.split("\n")
    hand = {}

    print(hand_txt[1])
    hand['date'] = hand_txt[0].split(": ")[1]
    hand['game_id'] = hand_txt[1].split(": ")[1].split(" ")[0]
    hand['variant'] = hand_txt[1].split("(")[1].split(")")[0]
    hand['table_name'] = hand_txt[1].split(")")[1].split("(")[0].replace(" ", "")
    hand['type_game'] = hand_txt[1].split("(")[2].split(")")[0]

    hand['button_seat'] = int(hand_txt[2].split("Seat ")[1].split(" ")[0])

    hand['players'] = []
    hand['players_seats'] = []
    hand['starting_stacks'] = []
    line = 3
    while line < len(hand_txt):
        if hand_txt[line].split(" ")[0] != "Seat":
            break
        player = hand_txt[line].split(": ")[1].split(" (")[0]
        seat_nb = int(hand_txt[line].split("Seat ")[1].split(":")[0])
        stack = float(hand_txt[line].split("(")[1].split(")")[0])
        hand['players'].append(player)
        hand['players_seats'].append(seat_nb)
        hand['starting_stacks'].append(stack)
        line += 1
    
    while line < len(hand_txt):
        if "small blind" in hand_txt[line]:
            break
        line += 1
    hand['player_small_blind'] = hand_txt[line].split("Player ")[1].split(" has")[0]
    hand['small_blind'] = float(hand_txt[line].split("(")[1].split(")")[0])
    
    while line < len(hand_txt):
        if "big blind" in hand_txt[line]:
            break
        line += 1
    hand['player_big_blind'] = hand_txt[line].split("Player ")[1].split(" has")[0]
    print(hand_txt[line])
    hand['big_blind'] = float(hand_txt[line].split("(")[1].split(")")[0])

    hand['player'] = player_name
    hand['cards_player'] = []
    
    while line < len(hand_txt):
        if "[" in hand_txt[line]:
            card = hand_txt[line].split("[")[1].split("]")[0]
            hand['cards_player'].append(card)
        line += 1
        if not 'received' in hand_txt[line]:
            break
    

    dealed_cards = {"flop": [], "turn": [], "river": []}
    actions = {'pre-flop': {'players': [], 'actions': [], 'values': []},
                'post-flop': {'players': [], 'actions': [], 'values': []},
                'post-turn': {'players': [], 'actions': [], 'values': []},
                'post-river': {'players': [], 'actions': [], 'values': []}}
    

    turn = 'pre-flop'
    while line < len(hand_txt):
        if "***" in hand_txt[line]:
            if "FLOP" in hand_txt[line]:
                dealed_cards['flop'] = hand_txt[line].split("[")[-1].split("]")[0].split(" ")
                turn = 'post-flop'
            elif "TURN" in hand_txt[line]:
                dealed_cards['turn'] = hand_txt[line].split("[")[-1].split("]")[0].split(" ")
                turn = 'post-turn'
            elif "RIVER" in hand_txt[line]:
                dealed_cards['river'] = hand_txt[line].split("[")[-1].split("]")[0].split(" ")
                turn = 'post-river'
        elif "Player" not in hand_txt[line]:
            break
        else:
            mapping_actions = {"bets": "cbr", "raises": "cbr", "checks": "cc", "folds": "f", "calls": "cc"}
            action = None
            # split on action
            for action_ in mapping_actions.keys():
                if action_ in hand_txt[line]:
                    action = action_
                    break
            player = hand_txt[line].split("Player ")[1].split(f" {action}")[0]
            
            value = None
            if "(" in hand_txt[line]:
                value = float(hand_txt[line].split("(")[1].split(")")[0])
            if action in mapping_actions:
                action = mapping_actions[action]
            
            actions[turn]['players'].append(player)
            actions[turn]['actions'].append(action)
            actions[turn]['values'].append(value)
        line += 1

    hand['dealed_cards'] = dealed_cards
    hand['actions'] = actions

    while line < len(hand_txt):
        if "Summary" in hand_txt[line]:
            break
        line += 1

    finishing_stack =  hand['starting_stacks'].copy()

    hand['card_shown_by_players'] = []
    while line < len(hand_txt):
        if 'Player' in hand_txt[line]:
            for keys in [' does', ' shows', ' mucks']:
                if keys in hand_txt[line]:
                    player = hand_txt[line].split("Player ")[1].split(keys)[0]
                    break
                player = hand_txt[line].split("Player ")[1].split(" ")[0]

            #print(player)
            bets = hand_txt[line].split("Bets: ")[1].split(" ")[0]
            bets = bets[:-1] if bets[-1] == '.' else bets
            bets = float(bets)
            collects = hand_txt[line].split("Collects: ")[1].split(" ")[0]
            collects = collects[:-1] if collects[-1] == '.' else collects
            collects = float(collects)
            card = None
            if '[' in hand_txt[line]:
                card = hand_txt[line].split("[")[1].split("]")[0]
            hand['card_shown_by_players'].append(card)
            
            finishing_stack[hand['players'].index(player)] -= bets
            finishing_stack[hand['players'].index(player)] += collects
        line += 1

    hand['finishing_stack'] = finishing_stack

    return hand


if __name__ == "__main__":
    PATH_DATA = Path(__file__).resolve().parents[2] / "data" / "poker_dataset" / "Export Holdem Manager 2.0 12292016131233.txt"
    print(PATH_DATA)
    hand = []
    
    with open(PATH_DATA, 'r') as f:
        hands_txt = f.read()
        hands_txt_list = hands_txt.split("\n\n")
        print(f"last file: {hands_txt_list[-1]}")
        for i in range(len(hands_txt_list) -1):
            if "PokerStars" in hands_txt_list[i]:
                continue
            hand.append(format_dataset_to_struct(hands_txt_list[i]))

    print(hand)
        