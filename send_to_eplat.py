import sys
import json
import requests


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


def main(input_json: dict, ctx_obj: dict):
    secrets = ctx_obj.get('secrets')
    eplat_address = secrets.get('eplat_address')
    eplat_domain = secrets.get('eplat_domain')
    eplat_user = secrets.get('eplat_user')
    eplat_password = secrets.get('eplat_password')
    target_eplat_integration = secrets.get('target_eplat_integration')

    geo_result_formated = '; '.join(
        [
            f'ip адрес {i.get("ip", "Не удалось определить")} принадлежит стране {i.get("geo", "Не удалось определить")}'
            for i in input_json['result'][0]['geo']
            ] 
        ) if input_json['result'][0] else "Произошла ошибка при обогащении"


    vt_result_formated = '; '.join(
        [
            f'Результат сканирования ip адреса {i.get("ip", "Не удалось определить")}: {i.get("result", "Не удалось определить")}'
            for i in input_json['result'][1]['vt']
            ] 
        ) if input_json['result'][1] else "Произошла ошибка при обогащении"

    token = get_eplat_token(eplat_address, eplat_domain, eplat_user, eplat_password)
    j = json.dumps({
        "src_geoip_country_name": geo_result_formated,
        "result_desc": vt_result_formated,
        "SIEM_id": input_json["result"][0]["SIEM_id"]
        })
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        status = requests.post(
            f"{eplat_address}/{target_eplat_integration}",
            headers=headers,
            data=j
            ).status_code

        input_json['import_status'] = status

    else:
        input_json['import_status'] = 'Ошибка при получении токена'

    print(json.dumps(input_json))


if __name__ == '__main__':
    main(
        json.loads(sys.argv[1]),
        json.loads(sys.argv[2])
    )
