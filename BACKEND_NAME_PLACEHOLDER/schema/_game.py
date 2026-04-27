from pydantic import BaseModel
from typing import Optional

class GameBase(BaseModel):
    player_x: str
    player_o: Optional[str] = None

class GameCreate(GameBase):
    pass

class GameFull(GameBase):
    id: int
    board: str
    current_player: str
    status: str
    winner: Optional[str]
    move_history: str

class MoveBase(BaseModel):
    game_id: int
    player: str
    position: int

class MoveCreate(MoveBase):
    pass

class MoveFull(MoveBase):
    id: int
