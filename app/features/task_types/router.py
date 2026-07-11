"""Add the task router stuff here.
Get all, Get one, Add one, Amend, Delete"""

from fastapi import APIRouter, Path
from typing import Annotated

router = APIRouter(
    prefix="/task-types",
    tags=["task_types"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_all_task_types():
    return {"temp": "all task types retrieved"}


@router.get("/{item_id}")
async def get_all_task_types(
    item_id: Annotated[int, Path(title="The ID of the task_type to get")],
):
    return {"temp": "a task type retrieved"}
