"""Simple CLI example"""
import argparse

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--name', '-n', default='world')
    args = p.parse_args(argv)
    print(f"Hello, {args.name}!")

if __name__ == '__main__':
    main()
