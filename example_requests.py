import requests


r = requests.get('https://jsonplaceholder.typicode.com/todos/1')

print(
    f'Объект класса Response: {type(r)}',
    f'Код ответа: {r.status_code}',
    f'Тело ответа текстом: {r.text}',
    f'Тело ответа в json: {r.json()}',
    sep='\n\n'
    )