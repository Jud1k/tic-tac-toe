import uuid

from asyncpg import Connection
from redis import Redis

from app.dao.uow import UnitOfWork
from app.models import Game
from app.schemas.game import GameCreate


class GameService:
    def __init__(self, connection: Connection, redis_client: Redis):
        self.uow = UnitOfWork(connection, redis_client)

    async def get_all_games(self) -> list[Game]:
        async with self.uow as uow:
            return await uow.games.get_all()

    async def get_game_by_id(self, game_id: uuid.UUID) -> Game | None:
        async with self.uow as uow:
            return await uow.games.get_by_id(game_id)

    async def create_game(self, game_in: GameCreate) -> Game:
        async with self.uow as uow:
            game = await uow.games.create(game_in)
            await uow.games.create_game_players(game.id, game_in.players)
            return game
