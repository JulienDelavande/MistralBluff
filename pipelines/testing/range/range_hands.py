import numpy as np
import random

def range_hands():
    '''Generate hands for all possible pairs (suited and off-suited)'''
    range_matrix = np.zeros((13, 13), dtype=object)
    suits = ["s", "h", "d", "c"]
    values = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
    
    for i in range(13):
        for j in range(13):
            if j > i:  # Suited hands
                color = random.choice(suits)
                card1, card2 = values[i] + color, values[j] + color
                range_matrix[i][j] = card1, card2
            else:  # Off-suited hands
                colors = random.sample(suits, 2)
                card1, card2 = values[i] + colors[0], values[j] + colors[1]
                range_matrix[i][j] = card1, card2

    return range_matrix

# Example
print(range_hands())
