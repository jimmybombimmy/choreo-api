from copy import deepcopy

from sqlalchemy.exc import NoResultFound
from sqlmodel import Session


from app.core.db.db import engine
from app.models.seed import LocalSeedCollection
from app.seed.test_data import (
    test_users,
    test_collections,
    test_task_lists,
    test_tasks,
    test_collection_task_list_memberships,
    test_user_collection_memberships,
    test_user_task_list_memberships,
    test_collection_invitations,
    test_task_list_invitations,
)
from app.services.user_service import create_user, delete_user
from app.services.collection_service import create_collection
from app.services.task_list_service import create_task_list
from app.services.task_service import create_task
from app.services.collection_task_list_membership_service import (
    create_collection_task_list_membership,
)
from app.services.user_collection_membership_service import (
    create_user_collection_membership,
)
from app.services.user_task_list_membership_service import (
    create_user_task_list_membership,
)
from app.services.collection_invitation import create_collection_invitation
from app.services.task_list_invitation import create_task_list_invitation

# To do:
# - √ Seed all test data
# - √ Add all seeded data to an object variable
# - √ Save this to a file
# - √ Add it to .gitignore
#   Turn your seed data objects into one big one to call that as one, rather than loads of separate ones.
# - separate your services our into singular functions
#   - create, get, delete
#   - Get rid of the rest
#   - Make sure you have an Enum to get your types right - e.g. returning one of User, Collection, etc.
# - Add in your test data to remove all previous test data by uuid
# - Add prints to tell you this is done
# - Ensure all types are created and present in models - this hasn't been done yet
# - Create a command script with pyproject to run this seed easier
# - Unit tests
# - Integration tests

with Session(engine) as session:
    seed_data = LocalSeedCollection(users=[], collections=[])

    # delete_user(UUID("852eac54-4d78-4f97-b311-6218d9ad1210"), session)

    for user in test_users:
        try:
            delete_user(user.id, session)
        except NoResultFound:  # better error?
            print(f"Couldn't find user to delete pre-seed. id = {user.id}")

    # -- Create separate functions for deletion and creation and call them here --

    for user in test_users:
        created_user = create_user(user, session)
        # without deepcopy, future session.refresh(user)'s flush it from memory and you won't find it in seed_data
        seed_data.users.append(deepcopy(created_user))

    for collection in test_collections:
        created_collection = create_collection(collection, session)
        seed_data.collections.append(deepcopy(created_collection))

    for task_list in test_task_lists:
        created_task_list = create_task_list(task_list, session)
        seed_data.task_lists.append(deepcopy(created_task_list))

    for task in test_tasks:
        created_task = create_task(task, session)
        seed_data.tasks.append(deepcopy(created_task))

    for ctlm in test_collection_task_list_memberships:
        created_ctlm = create_collection_task_list_membership(ctlm, session)
        seed_data.collection_task_list_memberships.append(deepcopy(created_ctlm))

    for utlm in test_user_task_list_memberships:
        created_utlm = create_user_task_list_membership(utlm, session)
        seed_data.user_task_list_memberships.append(deepcopy(created_utlm))

    for ucm in test_user_collection_memberships:
        created_ucm = create_user_collection_membership(ucm, session)
        seed_data.user_collection_memberships.append(deepcopy(created_ucm))

    for ci in test_collection_invitations:
        created_ci = create_collection_invitation(ci, session)
        seed_data.collection_invitations.append(deepcopy(created_ci))

    for tli in test_task_list_invitations:
        created_tli = create_task_list_invitation(tli, session)
        seed_data.task_list_invitations.append(deepcopy(created_tli))

    seed_dict = LocalSeedCollection.model_validate(seed_data).model_dump_json()

    with open("seed_data.json", "w") as f:
        f.write(seed_dict)

    # # retrieved_user = get_current_user(seed_data.users[0].id, session)
