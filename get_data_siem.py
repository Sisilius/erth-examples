import sys
import json
import requests
import warnings
warnings.filterwarnings("ignore")


def get_eplat_token(
        eplat_address: str,
        eplat_domain: str,
        eplat_user: str,
        eplat_password: str,
        ) -> str:

    token_request = requests.post(
                            f"{eplat_address}/api/getToken",
                            data={
                                'password': eplat_password,
                                'username': f"{eplat_domain}\{eplat_user}",
                                'grant_type': 'password'
                                })

    try:
        token = token_request.json().get('access_token')
    except Exception:
        token = None

    return token


def deep_get(_dict: dict, keys: list, default=None):
    for key in keys:
        if isinstance(_dict, dict):
            _dict = _dict.get(key, default)
        elif isinstance(_dict, list):
            try:
                _dict = _dict[key]
            except:
                return default
        else:
            return default
    return _dict


def main(input_json: dict, ctx_obj: dict):    
    SIEM_id = input_json['SIEM_id']    
    siem_pref, inc_number = SIEM_id.split('-')

    secrets = ctx_obj.get('secrets')
    eplat_address = secrets.get('eplat_address')
    eplat_domain = secrets.get('eplat_domain')
    eplat_user = secrets.get('eplat_user')
    eplat_password = secrets.get('eplat_password')
    source_eplat_integration = secrets.get('source_eplat_integration')
    target_eplat_integration = secrets.get('target_eplat_integration')

    token = get_eplat_token(eplat_address, eplat_domain, eplat_user, eplat_password)
    headers = {"Authorization": f"Bearer {token}"}

    main_export = requests.get(f'{eplat_address}/{source_eplat_integration}', headers=headers).json()
    siem = list(filter(lambda x: x['part'] == f'{siem_pref}-', main_export))[0]

    link, api_key, source = siem['link'], siem['key'], siem['source']

    if source == 'RuSIEM':
    
        def get_required_fields():
            inc = requests.get(f"{link}/api/v1/incidents/{inc_number}/fullinfo?_api_key={api_key}", verify=False).json()
            src_ip = deep_get(inc, ['metadata', 'src.ip', 'statistic'], False)

            return src_ip if src_ip else False

        src_ip = get_required_fields()
        if src_ip:
            inc = requests.get(f"{link}/api/v1/incidents/{inc_number}/fullinfo?_api_key={api_key}", verify=False).json()
            ips = deep_get(inc, ['metadata', 'src.ip', 'statistic'], [{"val": "Не найдено"}])
            input_json['ips'] = [{"ip":i['val']} for i in ips]
            input_json['result_all'] = True
            print(json.dumps(input_json))
        
        else:
            s = json.dumps({"result_all":False})
            requests.post(f'{eplat_address}/{target_eplat_integration}', data = s, headers=headers)
            print(s)


if __name__ == '__main__':
    main(
        json.loads(sys.argv[1]),
        json.loads(sys.argv[2])
        )
