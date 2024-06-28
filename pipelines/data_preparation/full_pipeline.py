from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from pipelines.data_preparation.cleaned_data import process_directory
from pipelines.data_preparation.format_api import create_training_dataset

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = ROOT_DIR / 'data/1_raw_data'
CLEANED_DATA_DIR = ROOT_DIR / 'data/2_cleaned_data'
PREPARED_DATA_DIR = ROOT_DIR / 'data/3_prepared_data'
FILE_NAME_1 = 'Export Holdem Manager 2.0 12292016131233.txt'
FILE_NAME_2 = 'Export Holdem Manager 2.0 12302016144830.txt'
OUTPUT_FILE_NAME_TRAIN = 'anatole_data_train.json'
OUTPUT_FILE_NAME_TEST = 'anatole_data_test.json'

def full_pipeline(raw_data_dir : Path = RAW_DATA_DIR, 
                  cleaned_data_dir : Path = CLEANED_DATA_DIR, 
                  prepared_data_dir : Path = PREPARED_DATA_DIR, 
                  file_names : list[str] = [FILE_NAME_1, FILE_NAME_2],
                  output_file_name_train : str = OUTPUT_FILE_NAME_TRAIN, 
                  output_file_name_test : str = OUTPUT_FILE_NAME_TEST):
    """
    Process the raw data, create training datasets, merge them, and split them into training and test sets.

    Args:
    raw_data_dir (Path): Path to the raw data directory.
    cleaned_data_dir (Path): Path to the cleaned data directory.
    prepared_data_dir (Path): Path to the prepared data directory.
    file_names (list[str]): List of file names to process.
    output_file_name_train (str): Name of the output file for the training dataset.
    output_file_name_test (str): Name of the output file for the test dataset.
    """
    # Process the raw data
    process_directory(raw_data_dir, cleaned_data_dir)
    file_paths = [cleaned_data_dir / file_name for file_name in file_names]

    # Create datasets from both files
    training_dfs = [create_training_dataset(file_path) for file_path in file_paths]
 
    # Merge the two datasets
    merged_df = pd.concat(training_dfs, ignore_index=True)
    merged_df.instruction = merged_df.instruction + "\nPlayer IlxxxlI"
    merged_df['input']=""
    merged_df = merged_df[['instruction', 'input', 'output']]

    # Split the merged dataset into training and test sets
    train, test = train_test_split(merged_df, test_size=0.1, random_state=0)
    train.to_json(prepared_data_dir / output_file_name_train, orient='records', lines=True)
    test.to_json(prepared_data_dir / output_file_name_test, orient='records', lines=True)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--raw_data_dir', type=str, required=False, default=RAW_DATA_DIR)
    parser.add_argument('--cleaned_data_dir', type=str, required=False, default=CLEANED_DATA_DIR)
    parser.add_argument('--prepared_data_dir', type=str, required=False, default=PREPARED_DATA_DIR)
    parser.add_argument('--file_names', type=str, required=False, default=[FILE_NAME_1, FILE_NAME_2])
    parser.add_argument('--output_file_name_train', type=str, required=False, default=OUTPUT_FILE_NAME_TRAIN)
    parser.add_argument('--output_file_name_test', type=str, required=False, default=OUTPUT_FILE_NAME_TEST)
    args = parser.parse_args()

    full_pipeline(Path(args.raw_data_dir),
                    Path(args.cleaned_data_dir),
                    Path(args.prepared_data_dir),
                    args.file_names,
                    args.output_file_name_train,
                    args.output_file_name_test)
    
