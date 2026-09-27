from typing import TypeAlias
from uuid import UUID


class FakeModel:
    def __init__(self, id, foo):
        self.id = id
        self.foo = foo


test_uuid = UUID("e97943d1-b1c1-4ab6-898a-c2344a6b5b1a")

fake_entry = FakeModel(id=test_uuid, foo="bar")

MockChoreoModel: TypeAlias = FakeModel
