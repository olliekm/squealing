import argparse
from chatting import question

def print_hi():
    print("hi")

def main():

    parser = argparse.ArgumentParser(
                        prog='sqling',
                        description='interact with your data with natural language',
                        epilog='YAHOO')    # Add a positional argument
    FUNCTION_MAP = {'question' : question,
                    'open' : print_hi }

    parser.add_argument('run', choices=FUNCTION_MAP.keys())

    args = parser.parse_args()

    func = FUNCTION_MAP[args.run]
    func()

if __name__ == "__main__":
    main()