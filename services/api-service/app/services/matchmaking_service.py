import datetime
import uuid

from loguru import logger
from redis import Redis

from app.schemas.game import Game, GameStatus


class MatchmakingService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def find_or_create_game(user_id: uuid.UUID, redis: Redis) -> Game:
        redis.register_script()
        active_game_data = await redis.get(f"player:{str(user_id)}:game")
        if active_game_data:
            return Game.model_validate_json(active_game_data)
        waiting_game_id = await redis.spop("games:waiting")  # pyright: ignore[reportGeneralTypeIssues]
        if waiting_game_id:
            new_game = Game(
                game_id=waiting_game_id,
                player_o_id=user_id,
                status=GameStatus.PLAYING,
                board=[None for _ in range(9)],
                created_at=datetime.datetime.now(),
            )
            await redis.setex(
                f"game:{waiting_game_id}", 3600, new_game.model_dump_json()
            )
            redis.register_script()
            await redis.set("player:")
            logger.info(f"Create new game with {waiting_game_id} ID ")
            return new_game
        new_waiting_game_id = uuid.uuid7()
        await redis.sadd("games:waiting", str(new_waiting_game_id))  # pyright: ignore[reportGeneralTypeIssues]
        logger.info(f"Add new game with {new_waiting_game_id} ID to waiting set")
        return Game(game_id=new_waiting_game_id)
