from typing import List, Optional
from pydantic import BaseModel

class DealedCards(BaseModel):
    flop: List[str]
    turn: List[str]
    river: List[str]

class Actions(BaseModel):
    players: List[str]
    actions: List[str]
    value: List[Optional[float]]

class GameActions(BaseModel):
    pre_flop: Actions
    post_flop: Actions
    post_turn: Actions
    post_river: Actions

class PokerGame(BaseModel):
    variant: str
    game_id: int
    hand_nb: int
    small_blind: float
    big_blind: float
    min_bet: float
    players: List[str]
    starting_stacks: List[float]
    players_seats: List[int]
    button_seat: int
    player_small_blind: str
    player_big_blind: str
    player: str
    cards_player: List[str]
    dealed_cards: DealedCards
    actions: GameActions
    winners: List[str]
    finishing_stacks: List[float]
    card_shown_by_players: List[Optional[str]]
