import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)

from app.api.deps import GameServiceDep, RedisClientDep, get_current_user_id_ws
from app.schemas.game import GameCreate, GameRead


router = APIRouter(prefix="/games", tags=["Game"])


# @router.websocket("/game")
# async def manage_game_lifecycle(
#     websocket: WebSocket,
#     redis: RedisClientDep,
#     current_user_id: int = Depends(get_current_user_id_ws),
# ):
#     await websocket.accept()
#     try:
#         while True:
#             ws_data = await websocket.receive_text()
#             logger.debug(ws_data)
#             game_data = Game.model_validate_json(ws_data, by_alias=True)
#             match game_data.status:
#                 case GameStatus.WAITING:
#                     game = await find_or_create_game(current_user_id, redis)
#                     await websocket.send_json(game.model_dump_json())
#                 case GameStatus.PLAYING:
#                     ...
#                 case GameStatus.FINISHED:
#                     ...
#     except WebSocketDisconnect:
#         ...


@router.get("/", response_model=list[GameRead])
async def get_all_games(
    game_service: GameServiceDep,
) -> list[GameRead]:
    return await game_service.get_all_games()


@router.get("/{game_id}", response_model=GameRead)
async def get_game_by_id(
    game_service: GameServiceDep,
    game_id: uuid.UUID,
) -> GameRead:
    game = await game_service.get_game_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Game not found"
        )
    return game


@router.post("/", response_model=GameRead, status_code=status.HTTP_201_CREATED)
async def create_game(
    game_service: GameServiceDep,
    game_in: GameCreate,
) -> GameRead:
    return await game_service.create_game(game_in)
