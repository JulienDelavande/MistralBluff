import os
import sys
from parse_hand import parse_hand
from anonymize_hand import anonymize_hand
from split_hand_by_actions import split_hand_by_actions
from format_hand_into_context_response import format_hand_into_context_response
from pathlib import Path
import json


DATA_PATH_ABS_PLURIBUS = "data/poker-hand-histories/data/pluribus/"
PATH_DUMB_JSON = "data/pluribus_data_prepared__v1_no_history.json"

data_path_pluribus = Path(__file__).resolve().parents[2] / DATA_PATH_ABS_PLURIBUS
data_path_pluribus = Path(__file__).resolve().parents[2] / DATA_PATH_ABS_PLURIBUS

def pipeline_data_prep_pluribus(no_history=True, player_name='Pluribus'):
    list_context_answers = []

    for folder in os.listdir(data_path_pluribus):
        for file_hand in os.listdir(data_path_pluribus / folder):
            hand = parse_hand(data_path_pluribus / folder / file_hand)
            player_idx = "p" + str(hand['players'].index(player_name))
            hand_anon = anonymize_hand(hand, player_idx)
            hand_stop_on_action_list, rest_of_action_list = split_hand_by_actions(hand_anon, player_idx)
            for i in range(len(hand_stop_on_action_list)):
                list_context_answers.append(format_hand_into_context_response(hand_stop_on_action_list[i], rest_of_action_list[i], player_idx))

    return list_context_answers

if __name__ == "__main__":
    #dumb json
    data = pipeline_data_prep_pluribus()
    with open(PATH_DUMB_JSON, 'w') as f:
        json.dump(data, f, indent=4)
