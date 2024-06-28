def compute_pfr(games, player="IlxxxlI"):
   """entrée: liste de formated game. 
   Calcule de la pre flop raise pour un set de partie"""
   total_hands = 0
   preflop_raises = 0
   for game in games:
       
        if player not in game["players"]:
            return 'mauvais nom de joueurs'

        player_index = game["actions"]["pre-flop"]["players"].index(player)
        preflop_actions = game["actions"]["pre-flop"]["actions"][player_index]

        if "cbr" in preflop_actions:
            preflop_raises += 1
        total_hands +=1
   # Calculate PFR
   if total_hands == 0:
       return 0
   else:
       pfr = (preflop_raises / total_hands)*100
       print("compute pfr, Ideally, it should be 2 or 3%: " + pfr)
       return pfr