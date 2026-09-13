from sqlmodel import Session

from app.core.db import engine
from app.seed.test_data import seed_test_data, seed_deletable_data
from app.services.services import create_entry, delete_entry

from app.types.models import ChoreoModel

# To do:
# - √ Seed all test data
# - √ Add all seeded data to an object variable
# - √ Save this to a file
# - √ Add it to .gitignore
# - √ Turn your seed data objects into one big one to call that as one, rather than loads of separate ones.
# - √ separate your services our into singular functions
#   - √ create, get, delete
#   - √ Get rid of the rest
#   - √ Make sure you have an Enum to get your types right - e.g. returning one of User, Collection, etc.
# - √ Add in your test data to remove all previous test data by uuid
# - √ Add prints to tell you this is done
# - √ Ensure all types are created and present in models - this hasn't been done yet
# - Unit tests
# - Integration tests

with Session(engine) as session:
    print("Deleting any seed entries that exist")
    for model in seed_deletable_data:
        model_name = type(model[0]).__name__
        m: type[ChoreoModel] = type(model[0])
        for entry in model:
            delete_entry(entry.id, m, session)

    print("Seeding database")
    for model in seed_test_data:
        model_name = type(model[0]).__name__
        for entry in model:
            created_entry = create_entry(entry, session)

    print("Successfully seeded database")
