def test_get_session_yields_session(blank_object_mock, get_session_mock):

    assert next(get_session_mock) == blank_object_mock
