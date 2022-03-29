import json
import sys
import requests
import time


def main(input_json: dict, ctx_obj: dict):
    ip = input_json['ip']

    secrets = ctx_obj.get('secrets')
    api_key_virustotal = secrets.get('vt_api_key')

    result_counter = {}

    data = {'url': ip}
    api_url = 'https://www.virustotal.com/api/v3/urls'
    headers = {'x-apikey': api_key_virustotal}
    response_query = requests.post(api_url, headers=headers, data=data)
    if response_query.status_code != 200:
        input_json['result'] = response_query.json()
        print(json.dumps(input_json))
        return

    while True:
        api_url = f'https://www.virustotal.com/api/v3/analyses/{response_query.json()["data"]["id"]}'
        headers = {'x-apikey': api_key_virustotal}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response['data']['attributes']['status'] == "completed":
                for i in response['data']['attributes']['results']:
                    if response['data']['attributes']['results'][i]['result'] in result_counter:
                        result_counter[response['data']['attributes']['results'][i]['result']] += 1
                    else:
                        result_counter[response['data']['attributes']['results'][i]['result']] = 1
                break
            else:
                time.sleep(5)
        else:
            time.sleep(5)

    input_json['result'] = str(result_counter)
    print(json.dumps(input_json))


if __name__ == '__main__':
    main(
        json.loads(sys.argv[1]),
        json.loads(sys.argv[2])
        )
