from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ._base import Base
from ._user import User

class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_x: Mapped[str] = mapped_column(String(50), ForeignKey("users.user_name"), nullable=False)
    player_o: Mapped[str] = mapped_column(String(50), ForeignKey("users.user_name"), nullable=True)
    board: Mapped[str] = mapped_column(String(9), default=" " * 9)  # 9-char string for board
    current_player: Mapped[str] = mapped_column(String(1), default="X")
    status: Mapped[str] = mapped_column(String(20), default="waiting")  # waiting, in_progress, finished
    winner: Mapped[str] = mapped_column(String(1), nullable=True)  # X, O, or None
    move_history: Mapped[str] = mapped_column(String(100), default="")  # comma-separated positions

    player_x_rel = relationship("User", foreign_keys=[player_x])
    player_o_rel = relationship("User", foreign_keys=[player_o])

    def __repr__(self):
        return f"Game(id={self.id}, player_x={self.player_x}, player_o={self.player_o}, board='{self.board}', status='{self.status}', winner={self.winner})"

class Move(Base):
    __tablename__ = "moves"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey("games.id"), nullable=False)
    player: Mapped[str] = mapped_column(String(1), nullable=False)  # X or O
    position: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-9

    def __repr__(self):
        return f"Move(id={self.id}, game_id={self.game_id}, player={self.player}, position={self.position})"
