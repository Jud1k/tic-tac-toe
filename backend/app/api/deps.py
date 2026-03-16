from pathlib import Path
import jwt
import asyncpg
from typing import Annotated, Any, AsyncGenerator
from fastapi import Depends, HTTPException, Query, WebSocketException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from redis import Redis

from app.core.database import database
from app.core.settings import settings
from app.schemas.user import UserRead
from app.services.game import GameService
from app.services.player import PlayerService
from app.core.redis import redis_client
from app.services.user import UserService

REDIS_SCRIPTS_DIR = Path(__file__).parent / "redis_scripts"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login/access-token")


async def get_db() -> AsyncGenerator[asyncpg.Connection, Any]:
    async with database.pool.acquire() as conn:
        yield conn


DbConnectionDep = Annotated[asyncpg.Connection, Depends(get_db)]


def get_redis_client() -> Redis:
    return redis_client


RedisClientDep = Annotated[Redis, Depends(get_redis_client)]


async def get_user_service(
    db_conn: DbConnectionDep, redis_client: RedisClientDep
) -> UserService:
    return UserService(db_conn, redis_client)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_player_service(
    db_conn: DbConnectionDep, redis_client: RedisClientDep
) -> PlayerService:
    return PlayerService(db_conn, redis_client)


PlayerServiceDep = Annotated[PlayerService, Depends(get_player_service)]


async def get_game_service(
    db_conn: DbConnectionDep, redis_client: RedisClientDep
) -> GameService:
    return GameService(db_conn, redis_client)


GameServiceDep = Annotated[GameService, Depends(get_game_service)]


async def get_current_user(
    user_service: UserServiceDep, token: str = Depends(oauth2_scheme)
) -> UserRead:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


CurrentUserDep = Annotated[UserRead, Depends(get_current_user)]


async def get_current_user_id_ws(token: str = Query(None)) -> str:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        player_id = payload.get("sub")
        if not player_id:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        return player_id
    except ExpiredSignatureError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    except PyJWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


# class RedisScripts:
#     def __init__(self, redis_client: Redis):
#         self.matchmaking = redis_client.register_script(
#             (REDIS_SCRIPTS_DIR / "matchmaking.lua").read_text()
#         )


# scripts = RedisScripts(redis_client)


# def get_redis_scripts():
#     return scripts


# RedisScriptsDep = Annotated[RedisScripts, Depends(get_redis_scripts())]
