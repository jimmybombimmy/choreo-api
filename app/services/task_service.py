from app.core.db import SessionDep
from app.models.tasks import Task


def create_task(task: Task, session: SessionDep) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_current_task(user_id: Task, session: SessionDep):
    task = session.get(Task, user_id)
    print(f"task {task}")
    return task


def delete_user(task: Task, session: SessionDep):
    session.delete(task)
    session.commit()
