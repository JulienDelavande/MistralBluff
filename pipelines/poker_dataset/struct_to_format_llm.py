def turn_to_format_llm(hand, turn='pre-flop'):
    hand_turn = ""
    for i in range(len(hand['actions'][turn]['players'])):
        player_name = hand['actions'][turn]['players'][i]
        action = hand['actions'][turn]['actions'][i]
        value = hand['actions'][turn]['value'][i]

        if action == "cc":
            action = "checks"
        elif action == "f":
            action = "folds"
        elif action == "cbr":
            if turn != 'pre-flop' and 'cbr' not in hand['actions'][turn]['actions'][:i]:
                action = "bets"
            else:
                action = "raises"

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

    seats = ""
    seats_list = [f"Seat {hand['players_seats'][i]}: {hand['players'][i]} ({hand['starting_stacks'][i]})" for i in range(len(hand['players']))]
    seats = "\n".join(seats_list)

    hand_pre_flop = turn_to_format_llm(hand, 'pre-flop')
    hand_flop = turn_to_format_llm(hand, 'post-flop')
    hand_turn = turn_to_format_llm(hand, 'post-turn')
    hand_river = turn_to_format_llm(hand, 'post-river')

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
    
    if hand_turn:
        hand_formated += f"""*** FLOP ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}]
{hand_flop}"""
    if hand_turn:
        hand_formated += f"""*** TURN ***: [{hand['dealed_cards']['turn'][0]}]
{hand_turn}"""
    if hand_river:
        hand_formated += f"""*** RIVER ***: [{hand['dealed_cards']['river'][0]}]
{hand_river}"""

    return hand_formated


if __name__ == "__main__":
    hand = {
    'variant' : 'NT',
    'game_id' : 808894969,
    'hand_nb' : 0,

    'small_blind' : 0.50,
    'big_blind' : 1,
    'min_bet' : 0,

    'players' : ['Gargantuatua', 'LAGrinder', 'IlxxxlI', 'MrPink', 'MrBrown', 'Pluribus'],
    'starting_stacks' : [10000, 10000, 10000, 10000, 10000, 10000],
    'players_seats' : [1, 2, 3, 4, 5, 6],

    'button_seat' : 1,
    'player_small_blind' : 'Gargantuatua',
    'player_big_blind' : 'LAGrinder',

    'player' : 'IlxxxlI',
    'cards_player' : ['10h', '10c'],

    'dealed_cards' : {
                    'flop': ['Qs', '9c', '4s'],
                    'turn': ['As'],
                    'river': ['8d']
                   },


    'actions' : {'pre-flop' : {
                            'players': ['IlxxxlI', 'MrPink'],
                            'actions': ['f', 'f'], # f for fold, cc for check, cbr for bet/raise
                            'value': [None, None]}, # None for fold and check, value for bet/raise
                'post-flop' : {
                            'players': ['IlxxxlI', 'MrPink'],
                            'actions': ['cbr', 'cbr'],
                            'value': [10, 30]},
                'post-turn' : {
                            'players': ['IlxxxlI', 'MrPink'],
                            'actions': ['cc', 'cbr'],
                            'value': [10, 30]},
                'post-river' : {
                            'players': ['IlxxxlI', 'MrPink'],
                            'actions': ['cc', 'cbr'],
                            'value': [10, 30]
                                }
               },
    
    'finishing_stacks': [10112.5, 9775.0, 10000.0, 10000.0, 10112.5, 10000.0]}

    print(struct_to_format_llm(hand))




