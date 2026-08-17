from sqlmodel import Session

from copy import deepcopy


from app.core.db import engine
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
from app.services.user_service import create_user
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
# - Seed all test data
# - Add all seeded data to an object variable
# - Save this to a file
# - √ Add it to .gitignore
# - Add in your test data to remove all previous test data by uuid
# - Add prints to tell you this is done
# - Ensure all types are created and present in models - this hasn't been done yet
# - Unit tests
# - Integration tests

with Session(engine) as session:
    seed_data = LocalSeedCollection(users=[], collections=[])
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

    # retrieved_user = get_current_user(seed_data.users[0].id, session)
