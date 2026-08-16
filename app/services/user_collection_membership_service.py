from app.core.db import SessionDep
from app.models.user_collection_memberships import UserCollectionMembership


def create_user_collection_membership(
    user_collection_membership: UserCollectionMembership, session: SessionDep
) -> UserCollectionMembership:
    session.add(user_collection_membership)
    session.commit()
    session.refresh(user_collection_membership)
    return user_collection_membership


def delete_user(
    user_collection_membership: UserCollectionMembership, session: SessionDep
):
    session.delete(user_collection_membership)
    session.commit()
