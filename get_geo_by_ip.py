import sys
import json
from ipwhois import IPWhois


def main(input_json: dict):
    ip = input_json.get('ip')

    try:
        obj = IPWhois(ip)
        geo_info = obj.lookup_rdap()
        input_json['geo'] = True
        input_json['geo_info'] = geo_info['asn_country_code']
    except Exception:
        input_json['geo'] = False
        input_json['geo_info'] = 'Ошибка определения местоположения'

    print(json.dumps(input_json))


if __name__ == '__main__':
    main(json.loads(sys.argv[1]))
