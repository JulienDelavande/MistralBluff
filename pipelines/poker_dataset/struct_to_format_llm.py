def turn_to_format_llm(hand, turn='pre_flop'):
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
            if turn != 'pre_flop' and 'cbr' not in hand['actions'][turn]['actions'][:i]:
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
    
    if hand_turn:
        hand_formated += f"""*** FLOP ***: [{hand['dealed_cards']['flop'][0]} {hand['dealed_cards']['flop'][1]} {hand['dealed_cards']['flop'][2]}]
{hand_flop}"""
    if hand_turn:
        hand_formated += f"""*** TURN ***: [{hand['dealed_cards']['turn'][0]}]
{hand_turn}"""
    if hand_river:
        hand_formated += f"""*** RIVER ***: [{hand['dealed_cards']['river'][0]}]
{hand_river}"""
        
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

    print(struct_to_format_llm(data))




