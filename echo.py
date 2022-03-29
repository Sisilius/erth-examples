import sys
import json


def main(input_json: dict):
    print(json.dumps(input_json))


if __name__ == '__main__':
    main(json.loads(sys.argv[1]))
