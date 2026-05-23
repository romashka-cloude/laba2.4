import os


def xor_encrypt_decrypt(data, key):
    encrypted_data = bytearray()
    for b in data:
        encrypted_byte = b ^ key
        encrypted_data.append(encrypted_byte)
    return encrypted_data


def encrypt_file(filename, key):
    # Чтение содержимого файла
    with open(filename, 'rb') as f:
        file_data = f.read()

    # Шифрование данных
    encrypted_data = xor_encrypt_decrypt(file_data, key)

    # Сохранение зашифрованного файла
    encrypted_filename = filename.split('.')[0] + '.bin'
    with open(encrypted_filename, 'wb') as ef:
        ef.write(encrypted_data)

    print(f"Файл '{filename}' успешно зашифрован и сохранен как '{encrypted_filename}'.")


if __name__ == "__main__":
    file_to_upload = input("Введите путь к загружаемому файлу (.json или .xml): ")

    if not os.path.exists(file_to_upload):
        print("Файл не найден.")
    else:
        key = int(input("Введите ключ от 0 до 255: "))
        encrypt_file(file_to_upload, key)
