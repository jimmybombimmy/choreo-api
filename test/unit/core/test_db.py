from ..mocks import blank_object_mock


def test_get_session_yields_session(get_session_mock):

    assert next(get_session_mock) == blank_object_mock()
