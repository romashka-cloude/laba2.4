def serialize(obj):
    if isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            items.append(f'"{key}": {serialize(value)}')
        return '{' + ', '.join(items) + '}'
    elif isinstance(obj, list):
        items = [serialize(item) for item in obj]
        return '[' + ', '.join(items) + ']'
    elif isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif obj is None:
        return 'null'
    else:
            raise TypeError(f"Тип {type(obj)} не сериализуемый")


def deserialize(s):
    s = s.strip()
    if s.startswith('{'):
        obj = {}
        s = s[1:-1].strip()
        items = split_items(s)
        for item in items:
            key, value = item.split(':', 1)
            obj[unquote(key.strip())] = deserialize(value.strip())
        return obj
    elif s.startswith('['):
        lst = []
        s = s[1:-1].strip()  # Удаляем []
        items = split_items(s)
        for item in items:
            lst.append(deserialize(item.strip()))
        return lst
    elif s.startswith('"') and s.endswith('"'):
        return unquote(s)
    elif s == 'null':
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    raise ValueError(f"Недействительный JSON: {s}")


def pretty_print(obj, indent=0):
    if isinstance(obj, dict):
        result = ['{' + '\n']
        for key, value in obj.items():
            result.append(' ' * (indent + 2) + f'"{key}": ')
            result.append(pretty_print(value, indent + 2))
            result.append(',\n')
        result[-1] = result[-1][:-2] + '\n'
        result.append(' ' * indent + '}')
        return ''.join(result)
    elif isinstance(obj, list):
        result = ['[' + '\n']
        for item in obj:
            result.append(' ' * (indent + 2))
            result.append(pretty_print(item, indent + 2))
            result.append(',\n')
        result[-1] = result[-1][:-2] + '\n'
        result.append(' ' * indent + ']')
        return ''.join(result)
    elif isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif obj is None:
        return 'null'


def validate_json(s):
    try:
        deserialize(s)
        return True
    except Exception as e:
        return str(e)


def split_items(s):
    items = []
    brace_count = 0
    current_item = []

    for char in s:
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        elif char == '[':
            brace_count += 1
        elif char == ']':
            brace_count -= 1
        elif char == ',' and brace_count == 0:
            items.append(''.join(current_item).strip())
            current_item = []
            continue

        current_item.append(char)

    if current_item:
        items.append(''.join(current_item).strip())

    return items


def unquote(s):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t')
    return s


def read_json_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content


def write_json_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)


# Пример использования
if __name__ == "__main__":
    # Чтение JSON из файла
    input_filename = 'resourse/input.json'
    json_string = read_json_file(input_filename)

    # Десериализация
    deserialized = deserialize(json_string)

    print("Десериализация JSON:")
    print(deserialized)

    # Сериализация обратно в строку
    serialized = serialize(deserialized)

    # Запись JSON в новый файл
    output_filename = 'resourse/output.json'  # Укажите имя выходного файла
    write_json_file(output_filename, serialized)

    print("\nСериализация JSON записана в ", output_filename)

    # Pretty print
    print("\nОбычный JSON:")
    print(pretty_print(deserialized))

    # Валидация
    invalid_json = '{"name": "John", "age": 30,}'
    validation_result = validate_json(invalid_json)
    print("\nРезультат проверки:")
    print(validation_result)
