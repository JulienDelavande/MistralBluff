import requests
from mistralai import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv
import os
from pipelines.poker_dataset.struct_to_format_llm import struct_to_format_llm

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL") or "http://localhost:8000"


def play(card1, card2, position, mistral_settings=None):
    ''' Returns LLM's action given cards in hands and position at the table (UTG or BB)'''
    if position == 'UTG' :
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
        "current_street" : "pre_flop",
 
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

    elif position == 'BB':
        data = {   "variant" : "NT",
        "game_id" : 779460276,
        "hand_nb" : 0,
 
        "small_blind" : 0.25,
        "big_blind" : 0.50,
        "min_bet" : 0.25,
 
        "players" : ["n0hvn", "tbmfc", "naprimer", "Log_in", "IlxxxlI", "gmjohn", "MANTISGUYV10", "BiGFck"],
        "starting_stacks" : [55.50, 28.47, 55.06, 14.65, 20, 28.76, 58.24, 17],
        "players_seats" : [1, 2, 3, 4, 5, 7, 8, 9],
 
        "button_seat" : 3,
        "player_small_blind" : "Log_in",
        "player_big_blind" : "IlxxxlI",
 
        "player" : "IlxxxlI",
        "cards_player" : [card1, card2],
        "current_street" : "pre_flop",
 
        "dealed_cards" : {
                    "flop": [],
                    "turn": [],
                    "river": []
                   },
 
 
        "actions" : {"pre_flop" : {"players": ["gmjohn", "MANTISGUYV10", "BiGFck", "n0hvn", "tbmfc", "naprimer", "Log_in"],
                            "actions": ["f", "cc", "f", "f", "f", "f", "f"],
                            "value": [None, None, None, None, None, None, None]},
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
 "response"
 
        "winners" : [],
        "finishing_stacks": [],
        "card_shown_by_players" : []
        }
    
    #Envoie l'inférence dans le back  action = inference(data, argument_pour_inference)
    #Envoie le json data et reçoit l'action
    
    if not mistral_settings:
        route = "/predict_test"
        route = "/predict"
        response = requests.post(f'{BACKEND_URL}{route}', json=data)
        response_json = response.json()

        if 'response' in response_json:
            action = response_json['response']
            return action[0]
        else:
            raise ValueError(f"Error in response: {response_json}")
        
    else:
        client = mistral_settings['client']
        job = mistral_settings['job']
        hand_format_llm = struct_to_format_llm(data)
        print(hand_format_llm)
        chat_response = client.chat(
                model=job.fine_tuned_model,
                messages=[ChatMessage(role="user", content=hand_format_llm)],
                temperature = 0.3,
                max_tokens = 12,
            )
        action = chat_response.choices[0].message.content
        return action
        

