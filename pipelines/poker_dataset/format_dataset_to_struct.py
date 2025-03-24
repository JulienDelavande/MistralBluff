import json
from pathlib import Path

def format_dataset_to_struct(hand_txt, player_name='IlxxxlI'):
    
    # remove line with 'wait' or 'is timed out'
    hand_txt = hand_txt.split("\n")
    line_with_wait = [line for line in hand_txt if 'wait' in line]
    people_to_remove = [line.split("Player ")[1].split(" wait")[0] for line in line_with_wait]
    
    hand_txt = [line for line in hand_txt if 'wait' not in line and 'is timed out' not in line and 'mucks cards' not in line and 'posts' not in line and 'straddle' not in line]
    for people in people_to_remove:
        hand_txt = [line for line in hand_txt if people not in line]
    hand = {}

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
        if player in people_to_remove:
            line += 1
            continue
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
            mapping_actions = {"bets": "BET", "raises": "RAISE", "checks": "CHECK", "folds": "FOLD", "calls": "CALL", "allin": "ALLIN", "caps": "RAISE"}
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
    non_struct_hand = """Game started at: 2016/9/4 1:51:48
Game ID: 718931171 2/4 (PRR) Monopod (Short) - 2 (Hold'em)
Seat 7 is the button
Seat 1: BIGRAISE (174.47).
Seat 3: cracypoker (231.55).
Seat 5: bjv1105 (522.98).
Seat 6: IlxxxlI (80).
Seat 7: WalterBlack (125).
Seat 8: TheFront7 (265.95).
Player TheFront7 has small blind (2)
Player BIGRAISE has big blind (4)
Player TheFront7 received a card.
Player TheFront7 received a card.
Player BIGRAISE received a card.
Player BIGRAISE received a card.
Player cracypoker received a card.
Player cracypoker received a card.
Player bjv1105 received a card.
Player bjv1105 received a card.
Player IlxxxlI received card: [6c]
Player IlxxxlI received card: [8h]
Player WalterBlack received a card.
Player WalterBlack received a card.
Player cracypoker folds
Player bjv1105 folds
Player IlxxxlI folds
Player WalterBlack calls (4)
Player TheFront7 folds
Player BIGRAISE checks
*** FLOP ***: [10s Ac Ad]
Player BIGRAISE checks
Player WalterBlack bets (4)
Player BIGRAISE calls (4)
*** TURN ***: [10s Ac Ad] [4s]
Player BIGRAISE checks
Player WalterBlack bets (4)
Player BIGRAISE calls (4)
*** RIVER ***: [10s Ac Ad 4s] [2c]
Player BIGRAISE checks
Player WalterBlack checks
------ Summary ------
Pot: 25.75. Rake 0.17. JP fee 0.08
Board: [10s Ac Ad 4s 2c]
*Player BIGRAISE shows: Three Of Kind of As [As 3h]. Bets: 12. Collects: 25.75. Wins: 13.75.
Player cracypoker does not show cards.Bets: 0. Collects: 0. Wins: 0.
Player bjv1105 does not show cards.Bets: 0. Collects: 0. Wins: 0.
Player IlxxxlI does not show cards.Bets: 0. Collects: 0. Wins: 0.
Player WalterBlack shows: Two pairs. As and 9s [9h 9s]. Bets: 12. Collects: 0. Loses: 12.
Player TheFront7 does not show cards.Bets: 2. Collects: 0. Loses: 2.
Game ended at: 2016/9/4 1:53:2"""

    import os

    hand_format = format_dataset_to_struct(non_struct_hand)

    print(hand_format)

    PATH_DATA = Path(__file__).resolve().parents[2] / "data" / "raw" / "poker_dataset" / "Export Holdem Manager 2.0 12292016131233.txt"
    PATH_DATA = Path(__file__).resolve().parents[2] / "data" / "raw" / "poker_dataset"
    PATH_DATA_OUT = Path(__file__).resolve().parents[2] / "data" / "structured" / "poker_dataset" 
    hand = []
    
    files = [f for f in os.listdir(PATH_DATA) if os.path.isfile(os.path.join(PATH_DATA, f))]
    
    i = 0
    for file in files[2:]:
        print(f"Processing {file}")
        path_data = PATH_DATA / file
        with open(path_data, 'r') as f:
            hands_txt = f.read()
            hands_txt_list = hands_txt.split("\n\n\n\n")
            n = len(hands_txt_list)
            for j in range(n - 1):
                print(f"Processing hand {j}/{n}, {hands_txt_list[j].split('\n')[0]}")
                if "PokerStars" in hands_txt_list[j]:
                    continue
                with open(PATH_DATA_OUT / f"hand_{i}.json", 'w') as f:
                    hand = format_dataset_to_struct(hands_txt_list[j])
                    json.dump(hand, f, indent=4)
        #         hand.append(format_dataset_to_struct(hands_txt_list[i]))
                i += 1

    
        