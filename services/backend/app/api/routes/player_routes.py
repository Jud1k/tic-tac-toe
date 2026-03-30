import uuid

from fastapi import APIRouter, HTTPException, status
from app.api.deps import CurrentUserDep, PlayerServiceDep

from app.schemas.game import GameRead
from app.schemas.player import PlayerRead, PlayerUpdate, PlayerWithRank

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/me", response_model=PlayerRead)
async def get_me(current_user: CurrentUserDep, player_service: PlayerServiceDep):
    player = await player_service.get_player_by_id(current_user.id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    return player


@router.patch("/me", response_model=PlayerRead)
async def update_me(
    player_service: PlayerServiceDep,
    current_user: CurrentUserDep,
    player_in: PlayerUpdate,
):
    if player_in.username:
        existing_player = await player_service.get_player_by_username(
            player_in.username
        )
        if existing_player and existing_player.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
    player = await player_service.update_player(current_user.id, player_in)
    return player


@router.get("/me/rank", response_model=PlayerWithRank)
async def get_player_with_rank(
    current_user: CurrentUserDep, player_service: PlayerServiceDep
):
    player = await player_service.get_player_with_rank(current_user.id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    return player


@router.get("/me/recent-games", response_model=list[GameRead])
async def get_recent_games(
    player_service: PlayerServiceDep, current_user: CurrentUserDep
):
    return await player_service.get_games_summary_by_player_id(current_user.id)


@router.get("/", response_model=list[PlayerRead])
async def get_players(player_service: PlayerServiceDep):
    return await player_service.get_all_players()


@router.get("/leaderboard", response_model=list[PlayerWithRank])
async def get_leaderboard(player_service: PlayerServiceDep):
    return await player_service.get_leaderboard()


@router.get("/{player_id}", response_model=PlayerRead)
async def get_player(player_id: uuid.UUID, player_service: PlayerServiceDep):
    player = await player_service.get_player_by_id(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    return player
