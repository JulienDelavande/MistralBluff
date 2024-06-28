import pandas as pd
import re
from pathlib import Path
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = ROOT_DIR / 'data/1_raw_data'
CLEANED_DATA_DIR = ROOT_DIR / 'data/2_cleaned_data'
PREPARED_DATA_DIR = ROOT_DIR / 'data/3_prepared_data'
FILE_NAME_1 = 'Export Holdem Manager 2.0 12292016131233.txt'
FILE_NAME_2 = 'Export Holdem Manager 2.0 12302016144830.txt'
OUTPUT_FILE_NAME_TRAIN = 'anatole_data_train.json'
OUTPUT_FILE_NAME_TEST = 'anatole_data_test.json'

def process_game_for_training(game):
    """Process a game to extract training data points."""
    lines = game.split('\n')
    data = []
    context = []

    for line in lines:
        line = line.strip()  
        if not line:  # Skip lines vide
            continue
        
        if line.startswith('Player IlxxxlI'):
            if ('received card:' in line) or ('has small blind' in line) or ('has big blind' in line):
                context.append(line)
            else:
                action = line.split('Player IlxxxlI ')[1]
                if context:  # Only add data point if there's context
                    data.append({'instruction': '\n'.join(context), 'output': action})
                context.append(line)  # Add this action to context for future actions
        else:
            context.append(line)

    return data

def create_training_dataset(file_path):
    """Create a training dataset from a file."""
    with open(file_path, 'r') as file:
        content = file.read()

    games = re.split(r'Game started\n', content)
    all_data = []

    for game in games:
        if game.strip():  # Ignore empty games
            all_data.extend(process_game_for_training(game))

    df = pd.DataFrame(all_data)
    return df


if __name__ == '__main__':
    file_path1 = CLEANED_DATA_DIR / FILE_NAME_1
    file_path2 = CLEANED_DATA_DIR / FILE_NAME_2

    # Create datasets from both files
    training_df1 = create_training_dataset(file_path1)
    training_df2 = create_training_dataset(file_path2)

    # Merge the two datasets
    merged_df = pd.concat([training_df1, training_df2], ignore_index=True)
    merged_df.instruction = merged_df.instruction + "\nPlayer IlxxxlI"
    merged_df['input']=""
    merged_df = merged_df[['instruction', 'input', 'output']]

    train, test = train_test_split(merged_df, test_size=0.1, random_state=0)
    train.to_json(PREPARED_DATA_DIR / OUTPUT_FILE_NAME_TRAIN, orient='records', lines=True)
    test.to_json(PREPARED_DATA_DIR / OUTPUT_FILE_NAME_TEST, orient='records', lines=True)
