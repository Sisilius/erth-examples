import sys
import json


def main(input_json: dict):
    important_key = input_json.get('important_key')

    if important_key and isinstance(important_key, int):
        input_json['inc'] = important_key + 1
    elif important_key is None:
        input_json['inc'] = 'Ошибка! Ключ important_key не передан'
    else:
        input_json['inc'] = 'Ошибка! Ключ important_key не содержит число'
    
    print(json.dumps(input_json, ensure_ascii=False))


if __name__ == '__main__':
    main(json.loads(sys.argv[1]))
