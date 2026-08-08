from sqlmodel import Session

from copy import deepcopy


from app.core.db import engine
from app.models.seed import LocalSeedCollection
from app.services.user_service import create_user
from app.seed.test_data import new_users

# To do:
# - Seed all test data
# - Add all seeded data to an object variable
# - Save this to a file
# - Also print it when you seed
# - √ Add it to .gitignore
# - Add in your test data to remove all previous test data by uuid
# - Add prints to tell you this is done
# - Ensure all types are created and present in models - this hasn't been done yet
# - Unit tests
# - Integration tests

with Session(engine) as session:
    seed_data = LocalSeedCollection(users=[])
    for user in new_users:
        created_user = create_user(user, session)
        # without deepcopy, session.refresh(user) flushes it from memory and you won't find it in seed_data
        seed_data.users.append(deepcopy(created_user))

    seed_dict = LocalSeedCollection.model_validate(seed_data).model_dump_json()
    # retrieved_user = get_current_user(seed_data.users[0].id, session)

    with open("seed_data.json", "w") as f:
        f.write(seed_dict)
