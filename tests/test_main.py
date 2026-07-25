import sys
import re
import pytest
from python_cli import main, handle_http_request, validate_name, EXIT_SUCCESS, EXIT_INVALID_INPUT


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


# --- Edge case tests for validate_name ---

def test_validate_name_single_char():
    assert validate_name('A') is None


def test_validate_name_only_digits():
    assert validate_name('123') is None


def test_validate_name_leading_space():
    assert validate_name('  Alice') is None


def test_validate_name_trailing_space():
    assert validate_name('Alice  ') is None


def test_validate_name_newline():
    err = validate_name('Alice\nBob')
    assert err is not None


def test_validate_name_tab():
    err = validate_name('Alice\tBob')
    assert err is not None


def test_validate_name_unicode():
    err = validate_name('Ãlice')
    assert err is not None


def test_validate_name_very_long():
    long_name = 'A' * 10000
    assert validate_name(long_name) is None


def test_validate_name_special_chars_mixed():
    err = validate_name('hello world!')
    assert err is not None


def test_validate_name_only_hyphen():
    assert validate_name('-') is None


def test_validate_name_only_underscore():
    assert validate_name('_') is None


# --- Edge case tests for main CLI ---

def test_main_flag_without_value():
    with pytest.raises(SystemExit) as exc:
        main(['--name'])
    assert exc.value.code == 2


def test_main_unknown_flag():
    with pytest.raises(SystemExit):
        main(['--unknown'])


def test_main_help_flag():
    with pytest.raises(SystemExit) as exc:
        main(['--help'])
    assert exc.value.code == EXIT_SUCCESS


def test_main_multiple_name_args():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'Alice', '--name', 'Bob'])
    assert exc.value.code == EXIT_SUCCESS


def test_main_name_with_numbers():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'User123'])
    assert exc.value.code == EXIT_SUCCESS


def test_main_name_single_char():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'A'])
    assert exc.value.code == EXIT_SUCCESS


def test_main_name_very_long():
    long_name = 'A' * 10000
    with pytest.raises(SystemExit) as exc:
        main(['--name', long_name])
    assert exc.value.code == EXIT_SUCCESS


def test_main_name_tab(capsys):
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'bad\tname'])
    assert exc.value.code == EXIT_INVALID_INPUT
    captured = capsys.readouterr()
    assert 'Error:' in captured.err


def test_main_name_newline(capsys):
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'bad\nname'])
    assert exc.value.code == EXIT_INVALID_INPUT
    captured = capsys.readouterr()
    assert 'Error:' in captured.err


def test_main_name_unicode():
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'Ãlice'])
    assert exc.value.code == EXIT_INVALID_INPUT


def test_main_error_message_on_stderr(capsys):
    with pytest.raises(SystemExit):
        main(['--name', ''])
    captured = capsys.readouterr()
    assert captured.err.startswith('Error:')


# --- Edge case tests for HTTP handler ---

def test_http_delete_method():
    status, body = handle_http_request('DELETE')
    assert status == 405
    assert 'error' in body


def test_http_patch_method():
    status, body = handle_http_request('PATCH')
    assert status == 405
    assert 'error' in body


def test_http_get_with_json_body_ignored():
    status, body = handle_http_request('GET', json_body={'name': 'Bob'})
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_post_with_query_string_ignored():
    status, body = handle_http_request('POST', query_string={'name': 'Alice'})
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_empty_query_string():
    status, body = handle_http_request('GET', query_string={})
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_empty_json_body():
    status, body = handle_http_request('POST', json_body={})
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_none_json_body():
    status, body = handle_http_request('POST', json_body=None)
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_none_query_string():
    status, body = handle_http_request('GET', query_string=None)
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_get_with_extra_params():
    status, body = handle_http_request('GET', query_string={'name': 'Alice', 'extra': 'value'})
    assert status == 200
    assert body['message'] == 'Hello, Alice!'


def test_http_post_missing_name():
    status, body = handle_http_request('POST', json_body={'other': 'data'})
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_get_missing_name():
    status, body = handle_http_request('GET', query_string={'other': 'data'})
    assert status == 200
    assert body['message'] == 'Hello, world!'


def test_http_case_sensitive_method():
    status, body = handle_http_request('get')
    assert status == 405


def test_http_method_with_spaces():
    status, body = handle_http_request(' GET ')
    assert status == 405


def test_http_empty_method():
    status, body = handle_http_request('')
    assert status == 405


# --- Integration tests ---

def test_exit_success_value():
    assert EXIT_SUCCESS == 0


def test_exit_invalid_input_value():
    assert EXIT_INVALID_INPUT == 1


def test_full_cli_flow_valid(capsys):
    with pytest.raises(SystemExit) as exc:
        main(['--name', 'Alice'])
    assert exc.value.code == EXIT_SUCCESS
    captured = capsys.readouterr()
    assert 'Hello, Alice!' in captured.out


def test_full_cli_flow_invalid(capsys):
    with pytest.raises(SystemExit) as exc:
        main(['--name', ''])
    assert exc.value.code == EXIT_INVALID_INPUT
    captured = capsys.readouterr()
    assert 'Error:' in captured.err