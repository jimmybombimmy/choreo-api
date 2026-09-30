from sqlmodel import Session

from app.core.db import engine
from app.seed.test_data import seed_test_data, seed_deletable_data
from app.services.services import create_entry, delete_entry

from app.types.models import ChoreoModel

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
