import os
import pickle
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_range_matrices(directory):
    range_matrices = []
    for filename in os.listdir(directory):
        if filename.endswith(".pkl"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as file:
                range_matrix = pickle.load(file)
                range_matrices.append(range_matrix)
    return range_matrices

def count_actions(range_matrices):
    action_counts = [[defaultdict(int) for _ in range(13)] for _ in range(13)]
    
    for range_matrix in range_matrices:
        for i in range(13):
            for j in range(13):
                action = range_matrix[i][j].split()[0]
                action_counts[i][j][action] += 1
    
    return action_counts

def action_counts_to_dataframe(action_counts):
    data = {
        (i, j): {action: count for action, count in action_counts[i][j].items()}
        for i in range(13) for j in range(13)
    }
    
    df = pd.DataFrame.from_dict(data, orient='index').fillna(0).astype(int)
    return df

def plot_action_heatmap(action_counts, action):
    data = [[action_counts[i][j][action] for j in range(13)] for i in range(13)]
    plt.figure(figsize=(10, 8))
    sns.heatmap(data, annot=True, fmt="d", cmap="YlGnBu")
    plt.title(f"Heatmap of {action} counts")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.show()
