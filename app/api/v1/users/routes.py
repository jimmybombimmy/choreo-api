from fastapi import APIRouter

from app.services.services import get_all_entries
from app.db.base import SessionDep

from app.models.users import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_all_users(session: SessionDep):
    entries = get_all_entries(User, session)
    return entries
