from app.core.db import SessionDep
from app.models.collection_invitations import CollectionInvitation


def create_collection_invitation(
    collection_invitation: CollectionInvitation, session: SessionDep
) -> CollectionInvitation:
    session.add(collection_invitation)
    session.commit()
    session.refresh(collection_invitation)
    return collection_invitation


def delete_user(collection_invitation: CollectionInvitation, session: SessionDep):
    session.delete(collection_invitation)
    session.commit()
