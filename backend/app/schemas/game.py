import uuid

from app.models import GameResult, PlayerType
from app.schemas.base import CustomBaseModel
from app.schemas.player import PlayerSummary


# class GameStatus(str, Enum):
#     WAITING = "WAITING"
#     PLAYING = "PLAYING"
#     FINISHED = "FINISHED"


# Cell = Literal["X", "O"]


# class Game(CustomBaseModel):
#     game_id: uuid.UUID | None = None
#     player_x_id: uuid.UUID | None = None
#     player_o_id: uuid.UUID | None = None
#     status: GameStatus = GameStatus.WAITING
#     board: list[Cell | None] | None = None
#     current_turn: Cell | None = None
#     created_at: datetime.datetime | None = None
#     finished_at: datetime.datetime | None = None

class GamePlayerBase(CustomBaseModel):
    game_id: uuid.UUID
    player_id: uuid.UUID | None = None
    side: str
    type: PlayerType


class GamePlayerRead(GamePlayerBase):
    id: uuid.UUID
    player: PlayerSummary | None = None


class GamePlayerCreate(GamePlayerBase):
    pass

class GameBase(CustomBaseModel):
    id: uuid.UUID
    result: GameResult
    duration: int


class GameCreate(GameBase):
    players: list[GamePlayerCreate]


class GameRead(GameBase):
    players: list[GamePlayerRead]
