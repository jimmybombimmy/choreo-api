from sqlmodel import Session
from sqlalchemy.exc import NoResultFound

from app.db.base import engine
from app.scripts.seed.test_data import seed_test_data, seed_deletable_data
from app.services.services import create_entry, delete_entry
from app.types.models import ChoreoModel


def run_seed():
    with Session(engine) as session:
        print("Deleting any seed entries that exist")
        for model in seed_deletable_data:
            m: type[ChoreoModel] = type(model[0])
            for entry in model:
                try:
                    delete_entry(entry.id, m, session)
                except NoResultFound:
                    pass

        print("Seeding database")
        for model in seed_test_data:
            for entry in model:
                create_entry(entry, session)

        print("Successfully seeded database")


if __name__ == "__main__":
    run_seed()
