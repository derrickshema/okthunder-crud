from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..models.users import User

from .auth_routes import get_current_user

from ..db.session import get_session

from ..models.player import Player

# Create a new router object for player-related endpoints. /player for all routes in their url.
router = APIRouter(prefix="/player", tags=["Player"])

@router.post("/create", response_model=Player)
async def create_player(
    player: Player, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
    ):
    """
    Create a new player.
    """
    session.add(player)
    session.commit()
    session.refresh(player)
    return player

@router.get("/", response_model=list[Player])
async def get_players(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Retrieve all players.
    """
    players = session.exec(select(Player)).all()
    return players

@router.get("/{player_id}", response_model=Player)
def read_player(player_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Retrieve one player.
    """
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.put("/{player_id}", response_model=Player)
def update_player(player_id: int, updated_player: Player, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Update one player.
    """
    db_player = session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    for key, value in updated_player.model_dump(exclude_unset=True).items():
        setattr(db_player, key, value)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player

@router.delete("/{player_id}", response_model=None)
def delete_player(player_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """
    Delete one player.
    """
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    session.delete(player)
    session.commit()