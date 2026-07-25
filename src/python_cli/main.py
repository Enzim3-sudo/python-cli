"""Simple CLI example with input validation and error handling."""
import argparse
import re
import sys

EXIT_SUCCESS = 0
EXIT_INVALID_INPUT = 1

def validate_name(name):
    if not name or not name.strip():
        return "Name must not be empty."
    if not re.match(r'^[a-zA-Z0-9 _-]+$', name):
        return "Name must only contain letters, digits, spaces, hyphens, or underscores."
    return None

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--name', '-n', default='world')
    args = p.parse_args(argv)
    error = validate_name(args.name)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(EXIT_INVALID_INPUT)
    print(f"Hello, {args.name}!")
    sys.exit(EXIT_SUCCESS)

def handle_http_request(method, query_string=None, json_body=None):
    if method not in ('GET', 'POST'):
        return 405, {"error": "Method not allowed."}
    name = 'world'
    if method == 'GET' and query_string:
        name = query_string.get('name', 'world')
    elif method == 'POST' and json_body:
        name = json_body.get('name', 'world')
    error = validate_name(name)
    if error:
        return 400, {"error": error}
    return 200, {"message": f"Hello, {name}!"}

if __name__ == '__main__':
    main()
