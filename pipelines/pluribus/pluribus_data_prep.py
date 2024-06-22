import os
from parse_hand import parse_hand
from anonymize_hand import anonymize_hand
from split_hand_by_actions import split_hand_by_actions
from format_hand_into_context_response import format_hand_into_context_response
from rename_file_to_sort import rename_file_to_sort
from pathlib import Path
import json

version = 5
history = "history_max10"
test = False
no_history = False
history_max = 10
rename = False

DATA_PATH_ABS_PLURIBUS = "data/poker-hand-histories/data/pluribus/"
PATH_DUMPED_JSON = f"data/data_prepared/pluribus__v{version}_{history}.json"

data_path_pluribus = Path(__file__).resolve().parents[2] / DATA_PATH_ABS_PLURIBUS


def pipeline_data_prep_pluribus(no_history=no_history, player_name='Pluribus', history_max=history_max, rename=rename):
    list_context_answers = []

    total_tokens = 0

    if rename:
        rename_file_to_sort(data_path_pluribus)

    for i, folder in enumerate(os.listdir(data_path_pluribus)):
        anonymized_hands_dict = []
        for j, file_hand in enumerate(os.listdir(data_path_pluribus / folder)):
            hand = parse_hand(data_path_pluribus / folder / file_hand)
            player_idx = "p" + str(hand['players'].index(player_name))
            hand_anon = anonymize_hand(hand, player_idx)
            anonymized_hands_dict.append(hand_anon)
            hand_stop_on_action_list, rest_of_action_list = split_hand_by_actions(hand_anon, player_idx)
            for k in range(len(hand_stop_on_action_list)):
                format_hand, tokens_used = format_hand_into_context_response(hand_stop_on_action_list[k], rest_of_action_list[k], 
                                                                player_idx, anonymized_hands_dict, no_history, history_max)
                list_context_answers.append(format_hand)
                total_tokens += tokens_used
            if test and j == 4:
                return list_context_answers, total_tokens
    

    return list_context_answers, total_tokens


if __name__ == "__main__":
    data, total_tokens = pipeline_data_prep_pluribus()
    print(f"Total tokens used: {total_tokens}")
    
    if test:
        #print(data)
        PATH_DUMPED_JSON = f"data/data_prepared/pluribus__v{version}_{history}__test.json"
        with open(PATH_DUMPED_JSON, 'w') as f:
            json.dump(data, f, indent=2, separators=(',', ':'))
    else:
    #dumb json
        with open(PATH_DUMPED_JSON, 'w') as f:
            json.dump(data, f, indent=2)
