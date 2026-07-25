import pytest
from python_cli import main, handle_http_request, validate_name, EXIT_INVALID_INPUT


def test_default_name():
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 0


def test_custom_name():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'Alice'])
    assert exc.value.code == 0


def test_short_name():
    with pytest.raises(SystemExit) as exc:
        main(['-n', 'Bob'])
    assert exc.value.code == 0


def test_name_with_spaces():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'Jane Doe'])
    assert exc.value.code == 0


def test_name_with_hyphen():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'Jean-Pierre'])
    assert exc.value.code == 0


def test_name_with_underscore():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'test_user'])
    assert exc.value.code == 0


def test_empty_name():
    with pytest.raises(SystemExit) as exc:
        main(['--name', ''])
    assert exc.value.code == EXIT_INVALID_INPUT


def test_whitespace_name():
    with pytest.raises(SystemExit) as exc:
        main(['--name', '   '])
    assert exc.value.code == EXIT_INVALID_INPUT


def test_name_with_special_chars():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'hello@world'])
    assert exc.value.code == EXIT_INVALID_INPUT


def test_name_with_symbols():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'foo!bar'])
    assert exc.value.code == EXIT_INVALID_INPUT


def test_validate_name_none():
    assert validate_name(None) is not None


def test_validate_name_empty():
    assert validate_name('') is not None


def test_validate_name_whitespace():
    assert validate_name('   ') is not None


def test_validate_name_valid():
    assert validate_name('Alice') is None


def test_validate_name_special_chars():
    assert validate_name('hello@world') is not None


def test_http_get_default():
    status, body = handle_http_request('GET')
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_get_with_name():
    status, body = handle_http_request('GET', query_string={'name': 'Alice'})
    assert status == 200
    assert body['message'] == 'Hello, Alice!'


def test_http_post_with_name():
    status, body = handle_http_request('POST', json_body={'name': 'Bob'})
    assert status == 200
    assert body['message'] == 'Hello, Bob!'


def test_http_invalid_method():
    status, body = handle_http_request('PUT')
    assert status == 405
    assert 'error' in body


def test_http_empty_name():
    status, body = handle_http_request('GET', query_string={'name': ''})
    assert status == 400
    assert 'error' in body


def test_http_bad_name():
    status, body = handle_http_request('GET', query_string={'name': 'bad@name'})
    assert status == 400
    assert 'error' in body