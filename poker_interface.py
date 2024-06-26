import streamlit as st

# Definition of default parameters

players_init = ["p1", "p2", "p3", "p4", "p5", "p6"]
blinds_options = ["Big Blind", "Small Blind", "None"]

### Module paramètres du jeu
st.title("Settings")

with st.expander("Game settings"):
    variant = st.selectbox("Variant", ["NT", "Omaha", "Holdem"])
    game_id = st.number_input("Game number", value=1)
    hand_nb = st.number_input("Hand number", value=1)
    small_blind = st.number_input("Small blind")
    big_blind = st.number_input("Big_blind")
    min_bet = st.number_input("Minimal bet")

### Module configuration de la table
st.title("Table configuration")

players = []
starting_stacks = []
player_seats = []

for i in range(len(players_init)):  # Assuming players_init has player names
    # Collect player information using columns
    col1, col2, col3 = st.columns(3)
    player_name = col1.text_input(f"Name", key=f"player_name_{i}")
    starting_stack = col2.number_input("Stack", min_value=0, key=f"starting_stack_{i}")
    seat_number = col3.selectbox("Seat", options=[i+1 for i in range(6)], key=f"seat_number_{i}")

    players.append(player_name)
    starting_stacks.append(starting_stack)
    player_seats.append(seat_number)


### Module positions
with st.expander("Positions"):
  button_seat = st.selectbox("Button", player_seats)
  player_small_blind = st.selectbox("Small Blind", players)
  player_big_blind = st.selectbox("Big Blind", players)


## Module cartes piochées
if "player_card" not in st.session_state:
  st.session_state["player_card"]  = []


with st.form("Cartes du joueur"):
  player = st.selectbox("Player playing", players)
  cards_hand_input = st.text_input("Cards (ex: Qs, 9c)")
  submit_button_player = st.form_submit_button("Refresh")

if submit_button_player:
    try:
        player_card = [cards_hand_input.split(", ")]
        st.session_state.update(player_card=player_card)
        st.write("Hand cards updated")
    except Exception as e:
        st.error(f"Erreur lors du traitement des entrées: {e}")

### Module cartes révélées
st.title("Dealed cards")
if "dealt_cards" not in st.session_state:
  st.session_state["dealt_cards"]  = {
      "flop": [],
      "turn": [],
      "river": [],
  }

# Input fields for each street (flop, turn, river)
with st.form("dealt_cards_form"):
    flop_cards_input = st.text_input("Flop (ex: Qs, 9c, 4s)", key="flop_input")
    turn_card_input = st.text_input("Turn (ex: As)", key="turn_input")
    river_card_input = st.text_input("River (ex: 8d)", key="river_input")
    submit_button_dealer = st.form_submit_button("Refresh")

if submit_button_dealer:
    dealt_cards = st.session_state["dealt_cards"]
    # Process input values
    try:
        # Split flop input and convert to list
        flop_cards = flop_cards_input.split(", ")
        dealt_cards["flop"] = [card for card in flop_cards]

        # Convert turn and river inputs to lists
        turn_card = turn_card_input
        river_card = river_card_input
        dealt_cards["turn"] = [turn_card] if turn_card else []
        dealt_cards["river"] = [river_card] if river_card else []

        # Display updated dealt cards dictionary
        st.session_state.update(dealt_cards=dealt_cards)
        st.write("Dealed cards updated")

    except Exception as e:
        st.error(f"Erreur lors du traitement des entrées: {e}")


### Module actions des joueurs
# Initialize session state to store actions
if "actions" not in st.session_state:
    st.session_state["actions"] = {
        "pre-flop": {"players": [], "actions": [], "value": []},
        "post-flop": {"players": [], "actions": [], "value": []},
        "post-turn": {"players": [], "actions": [], "value": []},
        "post-river": {"players": [], "actions": [], "value": []},
    }

actions = st.session_state["actions"]  # Use session state to store actions

# Title
st.title("Enregistrement des actions des joueurs")

# Input fields for each action
with st.form("player_action_form"):
    # Player name
    player_name_input = st.selectbox("Action's player", players)
    street_select = st.selectbox("Street", options=["pre-flop", "post-flop", "post-turn", "post-river"], key="street")
    action_type_select = st.selectbox("Action", options=["f", "crb", "cc"], key="action_type")
    #if action_type_select == "crb":
    raise_value_input = st.number_input("Value if raise", min_value=0, key="raise_value")

    # Submit button
    submit_button_action = st.form_submit_button("Add")

if submit_button_action:
    # Process input values
    player_name = player_name_input.strip()
    street = street_select
    action_type = action_type_select
    raise_value = raise_value_input if action_type == "crb" else None

    # Validate player name
    if not player_name:
        st.error("Nom du joueur obligatoire")
        
    # Append action to the corresponding street in the actions dictionary
    actions[street]["players"].append(player_name)
    actions[street]["actions"].append(action_type)
    actions[street]["value"].append(raise_value)

    # Update state to reflect changes
    st.session_state.update(actions=actions)
    st.write("Action added")



### Generate prompt
if st.button("Generate Json file"):
    data = {
    "variant": variant,
    "game_id": game_id,
    "hand_nb": hand_nb,

    "small_blind": small_blind,
    "big_blind": big_blind,
    "min_bet": min_bet,

    "players": players,
    "starting_stacks": starting_stacks,
    "player_seats": player_seats,

    "button_seat" : button_seat,
    "player_small_blind" : player_small_blind,
    "player_big_blind" : player_big_blind,

    "player" : player,
    "cards_player" : st.session_state["player_card"],
    
    "dealed_cards" : st.session_state["dealt_cards"], 
    "actions" : st.session_state["actions"],

    "winners" : [None],
    "finishing_stacks": [None, None, None, None, None, None],
    "card_shown_by_players" : [None, None, None, None, None, None]

    }
    # Affichage du JSON dans Streamlit
    st.json(data)

reset_button = st.button("Reset Game")

if reset_button:
    # Reset session state variables
    st.session_state["player_card"] = []  # Assuming player_card is a list
    st.session_state["dealt_cards"] = {
        "flop": [],
        "turn": [],
        "river": [],
    }  # Reset dealt_cards structure
    st.session_state["actions"] = {
        "pre-flop": {"players": [], "actions": [], "value": []},
        "post-flop": {"players": [], "actions": [], "value": []},
        "post-turn": {"players": [], "actions": [], "value": []},
        "post-river": {"players": [], "actions": [], "value": []},
    }  # Reset actions structure

    # Display confirmation message
    st.success("Game state has been reset!")
  
