from sqlmodel import Session

from app.core.db import engine
from app.models.users import User
from app.models.seed import LocalSeedCollection
from app.services.user_service import create_user, get_current_user

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

new_user = User(username="test-user", email="test@user.com", password="test")

with Session(engine) as session:
    seed_data = LocalSeedCollection(users=[])
    created_user = create_user(new_user, session)

    seed_data.users.append(created_user)

    seed_dict = LocalSeedCollection.model_validate(seed_data).model_dump_json()
    # retrieved_user = get_current_user(seed_data.users[0].id, session)

    with open("seed_data.json", "w") as f:
        f.write(seed_dict)
