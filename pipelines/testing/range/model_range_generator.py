from pipelines.testing.range_hands import range_hands
from pipelines.testing.range_testing import play

def model_range_generator(position, mistral_settings):
    """Fulfill a range with LLM's actions"""
    range_matrix = range_hands()
    for i in range(13):
        for j in range(13):
            card1, card2 = range_matrix[i][j]
            action = play(card1, card2, position, mistral_settings)
            range_matrix[i][j] = action
            print(f"Action for {card1} {card2} is {action}")

    return range_matrix