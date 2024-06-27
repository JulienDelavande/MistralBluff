def turn_to_format_llm(hand, turn='pre_flop'):
    hand_turn = ""
    for i in range(len(hand['actions'][turn]['players'])):
        player_name = hand['actions'][turn]['players'][i]
        action = hand['actions'][turn]['actions'][i]
        value = hand['actions'][turn]['value'][i]

        if action == "f":
            action = "folds"
        elif action == "cbr":
            if turn != 'pre_flop' and 'cbr' not in hand['actions'][turn]['actions'][:i]:
                action = "bets"
            else:
                action = "raises"
        elif action == "cc":
            if value:
                action = f"calls"
            else:
                action = "checks" 

        hand_turn += f"Player {player_name} {action}"
        if value:
            hand_turn += f" ({value})\n"
        else:
            hand_turn += "\n"
    return hand_turn


def struct_to_format_llm(hand):
    """
    Convert hand structure to format required by LLM model
    """

    ### Check format of hand
    current_street = hand["current_street"]
    if len(hand['players_seats']) != len(hand['players']):
        raise ValueError("Number of players and number of seats should be the same")
    if len(hand['starting_stacks']) != len(hand['players']):
        raise ValueError("Number of players and number of starting stacks should be the same")
    for street in hand['actions']:
        if len(hand['actions'][street]['players']) != len(hand['actions'][street]['actions']):
            raise ValueError(f"Number of players and number of actions should be the same for street {street}")
        if len(hand['actions'][street]['players']) != len(hand['actions'][street]['value']):
            raise ValueError(f"Number of players and number of values should be the same for street {street}")
    if len(hand['cards_player']) != 2:
        raise ValueError("Player should have 2 cards")
    if current_street == "flop":
        if len(hand['dealed_cards']['flop']) != 3:
            raise ValueError("Flop should have 3 cards")
    if current_street == "turn":
        if len(hand['dealed_cards']['turn']) != 1:
            raise ValueError("Turn should have 1 card")
    if current_street == "river":
        if len(hand['dealed_cards']['river']) != 1:
            raise ValueError("River should have 1 card")
    
    ### Format hand
    seats = ""
    seats_list = [f"Seat {hand['players_seats'][i]}: {hand['players'][i]} ({hand['starting_stacks'][i]})" for i in range(len(hand['players']))]
    seats = "\n".join(seats_list)
    

    hand_pre_flop = turn_to_format_llm(hand, 'pre_flop')
    hand_flop = turn_to_format_llm(hand, 'post_flop')
    hand_turn = turn_to_format_llm(hand, 'post_turn')
    hand_river = turn_to_format_llm(hand, 'post_river')

    variant = "PRR"
    table_name = "Kraken (short)"
    num_players = len(hand['players'])
    type_game = "Hold'em"


    hand_formated = f"""Game started:
Game ID: {hand['game_id']} {hand['small_blind']}/{hand['big_blind']} ({variant}) {table_name} - {num_players} ({type_game})
Seat {hand['button_seat']} is the button
{seats}
Player {hand['player_small_blind']} has small blind ({hand['small_blind']})
Player {hand['player_big_blind']} has big blind ({hand['big_blind']})
Player {hand['player']} received card: [{hand['cards_player'][0]}]
Player {hand['player']} received card: [{hand['cards_player'][1]}]
{hand_pre_flop}"""
    
    if hand_flop:
        hand_formated += f"""*** FLOP ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}]
{hand_flop}"""
    elif current_street == "flop":
        hand_formated += f"""*** FLOP ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}]\n"""

    if hand_turn:
        hand_formated += f"""*** TURN ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}] [{hand['dealed_cards']['turn'][0]}]
{hand_turn}"""
    elif current_street == "turn":
        hand_formated += f"""*** TURN ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}] [{hand['dealed_cards']['turn'][0]}]\n"""

    if hand_river:
        hand_formated += f"""*** RIVER ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]} {hand['dealed_cards']['flop'][2]}] [{hand['dealed_cards']['river'][0]}]
{hand_river}"""
    elif current_street == "river":
        hand_formated += f"""*** RIVER ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]} {hand['dealed_cards']['flop'][2]}] [{hand['dealed_cards']['river'][0]}]\n"""
        
        
    hand_formated += f"Player {hand['player']} "

    return hand_formated


if __name__ == "__main__":
    card1 = "2s"
    card2 = "3d"
    data = {   
        "variant" : "NT",
        "game_id" : 779459871,
        "hand_nb" : 0,
        "small_blind" : 0.25,
        "big_blind" : 0.50,
        "min_bet" : 0.25,
 
        "players" : ["n0hvn", "tbmfc", "naprimer", "Log_in", "IlxxxlI", "gmjohn", "MANTISGUYV10", "BiGFck"],
        "starting_stacks" : [55.50, 28.47, 55.31, 15.15, 20, 28.76, 57.49, 17],
        "players_seats" : [1, 2, 3, 4, 5, 7, 8, 9],
 
        "button_seat" : 2,
        "player_small_blind" : "naprimer",
        "player_big_blind" : "Log_in",
 
        "player" : "IlxxxlI",
        "cards_player" : [card1, card2],
        "current_street" : "river",
 
        "dealed_cards" : {
                    "flop": [],
                    "turn": [],
                    "river": []
                   },
 
 
        "actions" : {"pre_flop" : {"players": [],
                            "actions": [],
                            "value": []},
                "post_flop" : {
                            "players": [],
                            "actions": [],
                            "value": []},
                "post_turn" : {
                            "players": [],
                            "actions": [],
                            "value": []},
                "post_river" : {
                            "players": [],
                            "actions": [],
                            "value": []
                                }
               },
 
 
        "winners" : [],
        "finishing_stacks": [],
        "card_shown_by_players" : []
        }
    
    data = {'date': '2016/9/4 1:51:48', 
     'game_id': '718931171', 
     'variant': 'PRR', 
     'table_name': 'Monopod', 
     'type_game': 'Short', 
     'button_seat': 7, 
     'players': ['BIGRAISE', 'cracypoker', 'bjv1105', 'IlxxxlI', 'WalterBlack', 'TheFront7'], 
     'players_seats': [1, 3, 5, 6, 7, 8], 
     'starting_stacks': [174.47, 231.55, 522.98, 80.0, 125.0, 265.95], 
     'player_small_blind': 'TheFront7', 
     'small_blind': 2.0, 
     'player_big_blind': 'BIGRAISE', 
     'big_blind': 4.0, 
     'player': 'IlxxxlI',
     "current_street" : "river",
     'cards_player': ['6c', '8h'], 
     'dealed_cards': {
         'flop': ['10s', 'Ac', 'Ad'], 
         'turn': ['4s'], 
         'river': ['2c']}, 
     'actions': {
            'pre_flop': {
                'players': ['cracypoker', 'bjv1105', 'IlxxxlI', 'WalterBlack', 'TheFront7', 'BIGRAISE'], 
                'actions': ['f', 'f', 'f', 'cc', 'f', 'cc'], 
                'value': [None, None, None, 4.0, None, None]}, 
            'post_flop': {
                'players': ['BIGRAISE', 'WalterBlack', 'BIGRAISE'], 
                'actions': ['cc', 'cbr', 'cc'], 
                'value': [None, 4.0, 4.0]}, 
            'post_turn': {
                'players': ['BIGRAISE', 'WalterBlack', 'BIGRAISE'], 
                'actions': ['cc', 'cbr', 'cc'], 
                'value': [None, 4.0, 4.0]}, 
            'post_river': {
                'players': ['BIGRAISE', 'WalterBlack'], 
                'actions': ['cc', 'cc'], 
                'value': [None, None]}}, 
     'card_shown_by_players': ['As 3h', None, None, None, '9h 9s', None], 
     'finishing_stack': [188.22, 231.55, 522.98, 80.0, 113.0, 263.95]}

    print(struct_to_format_llm(data))




