import sys
import json


def main(input_json: dict):
    # Тип исполнителя
    input_json['task_action']['assignee_type'] = input_json.get('assignee_type')
    # Роль исполнителя
    input_json['task_action']['role'] = input_json.get('role')
    # Группа исполнителей
    input_json['task_action']['group'] = input_json.get('group')
    # Пользователь-исполнитель
    input_json['task_action']['assignee'] = input_json.get('assignee')
    # Описание задачи
    input_json['task_action']['description'] = input_json.get('description')
    # Автор задачи
    input_json['task_action']['author'] = input_json.get('author')
    # Приоритет задачи
    input_json['task_action']['priority'] = input_json.get('priority')
    # Выполнить до этой даты
    input_json['task_action']['date_completion'] = input_json.get('date_completion')
    # Имя задачи. Пример, "name": "Тестирование импорта данных"
    input_json['task_action']['name'] = input_json.get('name')

    print(json.dumps(input_json))


if __name__ == '__main__':
    main(json.loads(sys.argv[1]))
