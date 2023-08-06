import argparse
from fastmodels.datavalidator.validator import validate_json

def main():
    parser = argparse.ArgumentParser(description='Validate a JSON string.')
    parser.add_argument('json_string', type=str, help='The JSON string to validate.')
    args = parser.parse_args()
    is_valid = validate_json(args.json_string)
    if is_valid:
        print('The JSON string is valid.')
    else:
        print('The JSON string is invalid.')

if __name__ == '__main__':
    main()
