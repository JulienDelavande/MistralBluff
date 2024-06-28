def is_legal_action(output_llm):
    """
    Entrée: 1 Sortie brut du llm. 
    Vérifie si le coup proposé par le llm fait partie du set de coup possible
    """
    valid_actions = {"bets", "calls", "raises", "allin", "checks", "caps", "folds"}
    if any(action in output_llm.split() for action in valid_actions):
        return True
    return False

def legal_actions(outputs_llm):
    """ Entrée: liste de sortie llm brute
    Compte le nombre de coups non autorisé 
    """
    count=0
    for output in outputs_llm: 
        if is_legal_action(output): 
            count+=1
    return count

# test_output="raises (2.3). <\s>"
# print('raises' in test_output.split())

import re
import pandas as pd

def parse_action(action): 
    """parser pour ne pas prendre en compte les montants joués"""
    action = action.strip()
    match= re.match(r'(\w+)', action)
    return match.group(1) if match else None


legal_moves = ['bets', 'calls', 'raises', 'allin', 'checks', 'folds', 'caps']
def compare_to_test(waited_outputs, llm_outputs):
    """ 
    Entrée: output test set brute, output llm
    à partir d'une list des résultats attendue vs résultat prédit créer une matrice de confusion
    """
    waited_normalized = [parse_action(action) for action in waited_outputs]
    llm_normalized = [parse_action(action) for action in llm_outputs]
    confusion_matrix = pd.DataFrame(0, index=legal_moves, columns=legal_moves)
 
    for waited, llm in zip(waited_normalized, llm_normalized):
        if waited in legal_moves and llm in legal_moves:
            confusion_matrix.at[waited, llm] += 1
    return confusion_matrix

def find_misclassifications(waited_outputs, llm_outputs, true_action="raises", predicted_action="folds"):     
    indices = []   
    for i, (waited, llm) in enumerate(zip(waited_outputs, llm_outputs)):         
        waited_norm = parse_action(waited)        
        llm_norm = parse_action(llm)        
        if waited_norm == true_action and llm_norm == predicted_action: 
            indices.append(i)
    return indices
 
# Test

# waited_outputs = [
#     "raises (3)",
#     "calls (2)",
#     "checks",
#     "bets (5)",
#     "folds"
# ]
 
# llm_outputs = [
#     "raises (5.4) <s>",
#     "calls (2)",
#     " checks", 
#     "bets (10)",
#     "folds"
# ]
# confusion_matrix = compare_to_test(waited_outputs, llm_outputs)
# print(confusion_matrix)

