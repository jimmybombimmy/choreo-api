from app.core.db.db import SessionDep
from app.models.collection_task_list_memberships import CollectionTaskListMembership


def create_collection_task_list_membership(
    collection_task_list_membership: CollectionTaskListMembership, session: SessionDep
) -> CollectionTaskListMembership:
    session.add(collection_task_list_membership)
    session.commit()
    session.refresh(collection_task_list_membership)
    return collection_task_list_membership


def delete_user(
    collection_task_list_membership: CollectionTaskListMembership, session: SessionDep
):
    session.delete(collection_task_list_membership)
    session.commit()
