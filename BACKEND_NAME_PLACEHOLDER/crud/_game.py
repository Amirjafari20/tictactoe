from sqlalchemy.orm import Session
from BACKEND_NAME_PLACEHOLDER.model import Game, Move, User
from BACKEND_NAME_PLACEHOLDER.schema import GameCreate, MoveCreate
from typing import List, Optional

class GameCrud:
    def __init__(self, db: Session):
        self.db = db

    def create_game(self, game: GameCreate) -> Game:
        db_game = Game(player_x=game.player_x, player_o=game.player_o)
        self.db.add(db_game)
        self.db.commit()
        self.db.refresh(db_game)
        return db_game

    def get_games(self) -> List[Game]:
        return self.db.query(Game).all()

    def get_game(self, game_id: int) -> Optional[Game]:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def delete_game(self, game_id: int) -> bool:
        game = self.get_game(game_id)
        if game:
            self.db.delete(game)
            self.db.commit()
            return True
        return False

    def add_move(self, move: MoveCreate) -> Move:
        db_move = Move(game_id=move.game_id, player=move.player, position=move.position)
        self.db.add(db_move)
        self.db.commit()
        self.db.refresh(db_move)
        return db_move

    def get_moves(self, game_id: int) -> List[Move]:
        return self.db.query(Move).filter(Move.game_id == game_id).all()
