import argparse

parser = argparse.ArgumentParser(
    description='Script that tests the arguments',
    epilog='''
EXAMPLES:
  py args_program.py --testo hello --testo1 world
  py args_program.py --testo foo
''',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument('--testo', type=str, help='A first variable to test argument adding')
parser.add_argument('--testo1', type=str, help='A sec variable to test argument adding')

args = parser.parse_args()

print(f'testo: {args.testo}')
print(f'testo1: {args.testo1}')