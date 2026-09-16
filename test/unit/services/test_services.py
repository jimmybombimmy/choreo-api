from app.services.services import create_entry


def FakeModel(entry):
    return entry


def test_fake_entry_adds_and_returns_user(session_mock):
    entry = FakeModel({id: 123})

    result = create_entry(entry, session_mock)

    assert result is entry
    assert session_mock.added is entry
    assert session_mock.committed
    assert session_mock.refreshed is entry
