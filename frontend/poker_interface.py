import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")


# Definition of default parameters
blinds_options = ["Big Blind", "Small Blind", "None"]

### Module paramètres du jeu
st.title("Settings")

with st.expander("Game settings"):
    variant = st.selectbox("Variant", ["NT", "Omaha", "Holdem"])
    game_id = st.number_input("Game number", value=1)
    small_blind = st.number_input("Small blind")
    big_blind = st.number_input("Big_blind")
    min_bet = st.number_input("Minimal bet")

col_number_of_players, col_hand_nb= st.sidebar.columns(2)
number_of_players = col_number_of_players.number_input("Number of players", min_value=2, max_value=22, value=6)
hand_nb = col_hand_nb.number_input("Hand number", value=1)

### Module configuration de la table
st.title("Table configuration")

players = []
starting_stacks = []
player_seats = []

for i in range(number_of_players):  # Assuming players_init has player names
    # Collect player information using columns
    col1, col2, col3 = st.columns(3)
    player_name = col1.text_input(f"Name", key=f"player_name_{i}")
    starting_stack = col2.number_input("Stack", min_value=0, key=f"starting_stack_{i}")
    seat_number = col3.selectbox("Seat", options=[i+1 for i in range(23)], key=f"seat_number_{i}", index=i)

    players.append(player_name)
    starting_stacks.append(starting_stack)
    player_seats.append(seat_number)


### Module positions
with st.expander("Positions"):
  button_seat = st.selectbox("Button", player_seats)
  player_small_blind = st.selectbox("Small Blind", players)
  player_big_blind = st.selectbox("Big Blind", players, index=1)


## Module cartes piochées
if "player_card" not in st.session_state:
  st.session_state["player_card"]  = []



with st.sidebar.form("Cartes du joueur"):
  col_player, col_cards_hand_input = st.columns(2)
  player = col_player.selectbox("Player playing", players)
  cards_hand_input = col_cards_hand_input.text_input("Cards (ex: Qs, 9c)")
  submit_button_player = st.form_submit_button("Refresh")

if submit_button_player:
    try:
        player_card = [cards_hand_input.split(", ")]
        st.session_state.update(player_card=player_card)
        st.write("Hand cards updated")
    except Exception as e:
        st.error(f"Erreur lors du traitement des entrées: {e}")

### Module cartes révélées
st.sidebar.title("Dealed cards")
if "dealt_cards" not in st.session_state:
  st.session_state["dealt_cards"]  = {
      "flop": [],
      "turn": [],
      "river": [],
  }

# Input fields for each street (flop, turn, river)
with st.sidebar.form("dealt_cards_form"):
    cards_reveiled = st.text_input("Flop, Turn, River (ex: Qs, 9c, 4s, As...)", key="card_reveiled")
    submit_button_dealer = st.form_submit_button("Refresh")

if submit_button_dealer:
    dealt_cards = st.session_state["dealt_cards"]
    # Process input values
    try:
        # Split flop input and convert to list
        cards = cards_reveiled.split(", ")
        dealt_cards["flop"] = cards[:3] if len(cards) >= 3 else []
        dealt_cards["turn"] = [cards[3]] if len(cards) >= 4 else []
        dealt_cards["river"] = [cards[4]] if len(cards) >= 5 else []

        # Display updated dealt cards dictionary
        st.session_state.update(dealt_cards=dealt_cards)
        st.write("Dealed cards updated")

    except Exception as e:
        st.error(f"Erreur lors du traitement des entrées: {e}")


### Module actions des joueurs
# Initialize session state to store actions
if "actions" not in st.session_state:
    st.session_state["actions"] = {
        "pre_flop": {"players": [], "actions": [], "value": []},
        "post_flop": {"players": [], "actions": [], "value": []},
        "post_turn": {"players": [], "actions": [], "value": []},
        "post_river": {"players": [], "actions": [], "value": []},
    }

actions = st.session_state["actions"]  # Use session state to store actions

# Title
st.title("Enregistrement des actions des joueurs")
preflop_cb_col, postflop_cb_col, postturn_cb_col, postriver_cb_col = st.columns(4)
pre_flop_cb = preflop_cb_col.checkbox("pre_flop")
post_flop_cb = postflop_cb_col.checkbox("post_flop")
post_turn_cb = postturn_cb_col.checkbox("post_turn")
post_river_cb = postriver_cb_col.checkbox("post_river")
turn_cb_list = [pre_flop_cb, post_flop_cb, post_turn_cb, post_river_cb]

dfs = {'pre_flop' : pd.DataFrame({
    "players": [""],
    "actions": [""],
    "value": [None],
}),
'post_flop' : pd.DataFrame({
    "players": [""],
    "actions": [""],
    "value": [None],
}),
'post_turn' : pd.DataFrame({
    "players": [""],
    "actions": [""],
    "value": [None],
}),
'post_river' : pd.DataFrame({
    "players": [""],
    "actions": [""],
    "value": [None],
})}

for cb_value, street in zip(turn_cb_list, actions.keys()):
    if cb_value:
        col_title, col_df = st.columns([0.2, 0.8])
        col_title.markdown(f"#### {street}")
        df_to_use = dfs[street]

        if actions[street]["players"] != []:
            df_to_use = pd.DataFrame({
                "players": actions[street]["players"],
                "actions": actions[street]["actions"],
                "value": actions[street]["value"]
            })

        edited_df = col_df.data_editor(
            df_to_use,
            column_config={
                "players": st.column_config.SelectboxColumn(
                    "Player",
                    help="The Player that played the action",
                    width="medium",
                    options=[player for player in players],
                    required=True,
                ),
                "actions": st.column_config.SelectboxColumn(
                    "Action",
                    help="The action played by the player",
                    width="medium",
                    options=["f", "cc", "cbr"],
                    required=True,
                ),
                "value": st.column_config.NumberColumn(
                    "value",
                ),
            },
            num_rows='dynamic',
            key=street
        )

        players_list = edited_df["players"].to_list()
        actions_list = edited_df["actions"].to_list()
        values_list = edited_df["value"].to_list()
        is_valide = players_list != [""] and actions_list != [""]

        if is_valide:
            new_actions = actions
            new_actions[street] = {
                "players": players_list,
                "actions": actions_list,
                "value": values_list
            }
            st.session_state.update(actions=new_actions)

if st.button("display actions"):
    print(f"actions = {actions}\n")


# Exemple de données que vous avez fournies
data = {
    "variant": variant,
    "game_id": game_id,
    "hand_nb": hand_nb,
    "small_blind": small_blind,
    "big_blind": big_blind,
    "min_bet": min_bet,
    "players": players,
    "starting_stacks": starting_stacks,
    "players_seats": player_seats,
    "button_seat": button_seat,
    "player_small_blind": player_small_blind,
    "player_big_blind": player_big_blind,
    "player": player,
    "cards_player": st.session_state["player_card"],
    "dealed_cards": st.session_state["dealt_cards"],
    "actions": st.session_state["actions"],
    "winners": [],
    "finishing_stacks": [],
    "card_shown_by_players": []
}

st.title("Poker Game Submission")

if st.button("Submit Game"):
    response = requests.post(f"{BACKEND_URL}/predict/", json=data)
    st.write(response.json())
                                            

### Generate prompt
if st.button("Generate Json file"):
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
        "pre_flop": {"players": [], "actions": [], "value": []},
        "post_flop": {"players": [], "actions": [], "value": []},
        "post_turn": {"players": [], "actions": [], "value": []},
        "post_river": {"players": [], "actions": [], "value": []},
    }  # Reset actions structure

    # Display confirmation message
    st.success("Game state has been reset!")


