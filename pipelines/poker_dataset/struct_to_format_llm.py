from pathlib import Path
import json

def struct_to_format_llm(hand, stop_turn=1):
    """
    Convert hand structure to format required by LLM model
    """

    ### Check format of hand
    # current_street = hand["current_street"]
    # if len(hand['players_seats']) != len(hand['players']):
    #     raise ValueError("Number of players and number of seats should be the same")
    # if len(hand['starting_stacks']) != len(hand['players']):
    #     raise ValueError("Number of players and number of starting stacks should be the same")
    # for street in hand['actions']:
    #     if len(hand['actions'][street]['players']) != len(hand['actions'][street]['actions']):
    #         raise ValueError(f"Number of players and number of actions should be the same for street {street}")
    #     if len(hand['actions'][street]['players']) != len(hand['actions'][street]['value']):
    #         raise ValueError(f"Number of players and number of values should be the same for street {street}")
    # if len(hand['cards_player']) != 2:
    #     raise ValueError("Player should have 2 cards")
    # if current_street == "flop":
    #     if len(hand['dealed_cards']['flop']) != 3:
    #         raise ValueError("Flop should have 3 cards")
    # if current_street == "turn":
    #     if len(hand['dealed_cards']['turn']) != 1:
    #         raise ValueError("Turn should have 1 card")
    # if current_street == "river":
    #     if len(hand['dealed_cards']['river']) != 1:
    #         raise ValueError("River should have 1 card")
    
    ### Format hand
    
    players_names_to_ano = {hand['players'][i]: f"P{i+1}" for i in range(len(hand['players']))}
    players_seat_to_ano = {hand['players_seats'][i]: f"P{i+1}" for i in range(len(hand['players']))}
    BB_amount = hand['big_blind']
    stacks_player = hand['starting_stacks'].copy()
    players_in_game = hand['players'].copy()
    
    out_str = ""
    # [TABLE_CONFIGURATION]
    table_config = f""" 
[TABLE_CONFIGURATION]
BTN={players_seat_to_ano[hand['button_seat']]}
SB={players_names_to_ano[hand['player_small_blind']]} 0.5BB
BB={players_names_to_ano[hand['player_big_blind']]} 1BB\n"""
    pot = 1.5*BB_amount
    turn = 0
    dealed_cards = []
    stacks_player[hand['players'].index(hand['player'])] -= 1*BB_amount
    stacks_player[hand['players'].index(hand['player_small_blind'])] -= 0.5*BB_amount
    out_str += table_config
    for street_key, street_upercase, steet in zip(['pre-flop', 'post-flop', 'post-turn', 'post-river'], ['PREFLOP', 'FLOP', 'TURN', 'RIVER'], [None, 'flop', 'turn', 'river']):
        # [STACKS]
        stacks_str, pot = compute_stacks(hand, pot, stacks_player, BB_amount, players_names_to_ano, players_in_game)
        out_str +=  stacks_str
        # [ACTIONS]
        dealed_cards += hand['dealed_cards'].get(steet, [])
        actions_str, stacks_player, pot, turn, value_strt = compute_actions(hand, hand['actions'][street_key], street_upercase, stacks_player, pot, players_names_to_ano, BB_amount, turn, stop_turn, dealed_cards, players_in_game)
        out_str += actions_str
        if value_strt:
            return out_str, value_strt
    return out_str, None
    
def compute_stacks(hand, pot, stacks_player, BB_amount, players_names_to_ano, players_in_game):
    stacks_str = "\n[STACKS]\n"
    for i, player in enumerate(hand['players']):
        if player not in players_in_game:
            continue
        stack_player_bb = stacks_player[i]/BB_amount
        stacks_str += f"{players_names_to_ano[hand['players'][i]]}: {stack_player_bb:.1f}BB"
        if hand['players'][i] == hand['player']:
            stacks_str += f" [{hand['cards_player'][0]} {hand['cards_player'][1]}]"
        stacks_str += "\n"
    pot_bb = pot/BB_amount
    stacks_str += f"POT={pot_bb:.1f}BB\n"
    return stacks_str, pot

def compute_actions(hand, street_actions, street, stacks_player, pot, players_names_to_ano, BB_amount, turn, stop_turn, deeled_cards, players_in_game):
    actions_str = f"\n[{street}]"
    if deeled_cards:
        actions_str += "["
        for card in deeled_cards:
            actions_str += f" {card}"
        actions_str += "]"
    actions_str += "\n"
    actions_str = actions_str.replace("[ ", "[")
    
    for i, player in enumerate(street_actions['players']):
        action = street_actions['actions'][i]
        
        value = street_actions['values'][i]
        value_str = ""
        if value:
            value_bb = int(value/BB_amount)
            value_str += f" {value_bb}BB\n"
        else:
            value_str += "\n"
        if action in ["BET", "RAISE", "CALL"]:
            stacks_player[hand['players'].index(player)] -= value
            pot += value
        elif action == 'ALLIN':
            stacks_player[hand['players'].index(player)] = 0
            pot += value
        elif action == 'FOLD':
            players_in_game.remove(player)
            
        if player == hand['player']:
            turn += 1
            if turn == stop_turn:
                actions_str += f"{players_names_to_ano[player]}: "
                return actions_str, stacks_player, pot, turn, f"{action}{value_str}"
        actions_str += f"{players_names_to_ano[player]}: {action}{value_str}"
    return actions_str, stacks_player, pot, turn, None
    
def old():
        pass
        #     variant = "PRR"
        #     table_name = "Kraken (short)"
        #     num_players = len(hand['players'])
        #     type_game = "Hold'em"

        #     seats = ""
        #     seats_list = [f"Seat {hand['players_seats'][i]}: {hand['players'][i]} ({hand['starting_stacks'][i]})" for i in range(len(hand['players']))]
        #     seats = "\n".join(seats_list)


        #     hand_formated = f"""Game started:
        # Game ID: {hand['game_id']} {hand['small_blind']}/{hand['big_blind']} ({variant}) {table_name} - {num_players} ({type_game})
        # Seat {hand['button_seat']} is the button
        # {seats}
        # Player {hand['player_small_blind']} has small blind ({hand['small_blind']})
        # Player {hand['player_big_blind']} has big blind ({hand['big_blind']})
        # Player {hand['player']} received card: [{hand['cards_player'][0]}]
        # Player {hand['player']} received card: [{hand['cards_player'][1]}]
        # {hand_pre_flop}"""
            
        #     if hand_flop:
        #         hand_formated += f"""*** FLOP ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}]
        # {hand_flop}"""
        #     elif current_street == "flop":
        #         hand_formated += f"""*** FLOP ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}]\n"""

        #     if hand_turn:
        #         hand_formated += f"""*** TURN ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}] [{hand['dealed_cards']['turn'][0]}]
        # {hand_turn}"""
        #     elif current_street == "turn":
        #         hand_formated += f"""*** TURN ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}] [{hand['dealed_cards']['turn'][0]}]\n"""

        #     if hand_river:
        #         hand_formated += f"""*** RIVER ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]} {hand['dealed_cards']['flop'][2]}] [{hand['dealed_cards']['river'][0]}]
        # {hand_river}"""
        #     elif current_street == "river":
        #         hand_formated += f"""*** RIVER ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]} {hand['dealed_cards']['flop'][2]}] [{hand['dealed_cards']['river'][0]}]\n"""
                
                
        #     hand_formated += f"Player {hand['player']} "

        #     return hand_formated

def count_nb_turn(hand):
    count = 0
    for street in hand['actions'].values():
        count += street['players'].count(hand['player'])
    return count

if __name__ == "__main__":
    PATH_DATA = Path(__file__).resolve().parents[2] / "data" / "structured" / "poker_dataset"
    PATH_DATA_OUT = Path(__file__).resolve().parents[2] / "data" / "train" / "poker_dataset"
    
    with open(PATH_DATA / "hand_8.json", "r") as f:
        hand = json.load(f)
    out_str, value_str = struct_to_format_llm(hand, 4)
    print(out_str)
    print(value_str)
    
    for file in PATH_DATA.glob("*.json"):
        print(f"Processing {file}")
        with open(file, "r") as f:
            hand = json.load(f)
        nb_turn = count_nb_turn(hand)
        for i in range(1, nb_turn+1):
            print(f"Processing turn {i}")
            out_str, value_str = struct_to_format_llm(hand, i)
            out = {'context': out_str, 'truth': value_str}
            name = file.name.split(".")[0]
            with open(PATH_DATA_OUT / f'{name}_{i}.json', "w") as f:
                json.dump(out, f)


"""
[TABLE_CONFIGURATION]
BTN=P7
SB=P1 0.5BB
BB=P2 1BB

[STACKS]
P1: 174.3BB
P2: 126.2BB
P3: 195.6BB
P4: 62.1BB [Ad Kd]
P5: 98.4BB
P6: 190.2BB
P7: 40.0BB
POT=1.5BB

[PREFLOP]
P3: FOLD
P4: RAISE 3BB
P5: CALL 3BB
P6: CALL 3BB
P7: FOLD
P1: FOLD
P2: FOLD

[STACKS]
P4: 58.6BB [Ad Kd]
P5: 94.9BB
P6: 186.7BB
POT=12.0BB

[FLOP][10d 2h 5s]
P4: CHECK
P5: CHECK
P6: CHECK

[STACKS]
P4: 58.6BB [Ad Kd]
P5: 94.9BB
P6: 186.7BB
POT=12.0BB

[TURN][10d 2h 5s 2c]
P4: CHECK
P5: CHECK
P6: CHECK

[STACKS]
P4: 58.6BB [Ad Kd]
P5: 94.9BB
P6: 186.7BB
POT=12.0BB

[RIVER][10d 2h 5s 2c 4d]
P4:
CHECK
"""