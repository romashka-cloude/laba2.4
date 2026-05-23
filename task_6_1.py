import json
import os


def cyclic_shift(value, shift):
    return ((value << shift) & 0xFF) | (value >> (8 - shift))


def encrypt_decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            byte = f_in.read(1)
            if not byte:
                break
            byte_value = byte[0]
            shifted_value = cyclic_shift(byte_value, 2)
            encrypted_byte = shifted_value ^ key
            f_out.write(bytes([encrypted_byte]))


def validate_json(file_path):
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True
    except ValueError:
        return False


def validate_xml(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Простейшая проверка на наличие открывающего и закрывающего тега
            if content.startswith('<?xml') and content.count('<') == content.count('>'):
                return True
            else:
                return False
    except Exception:
        return False


def process_file(file_path):
    if not os.path.exists(file_path):
        print("Файл не найден.")
        return

    file_type = file_path.split('.')[-1]

    if file_type == 'json' and validate_json(file_path):
        print(f"Получен корректный JSON файл: {file_path}")
    elif file_type == 'xml' and validate_xml(file_path):
        print(f"Получен корректный XML файл: {file_path}")
    else:
        print(f"Недопустимый файл: {file_path}")
        return

    # Шифрование файла
    key = int(input("Введите ключ от 0 до 255: "))
    output_file = file_path.split('.')[0] + '.bin'
    encrypt_decrypt_file(file_path, output_file, key)
    print(f"Файл '{file_path}' зашифрован и сохранен как '{output_file}'.")


if __name__ == "__main__":
    file_to_process = input("Введите путь к обрабатываемому файлу (.json или .xml): ")
    process_file(file_to_process)
