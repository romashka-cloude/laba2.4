def cyclic_shift(value, shift):
    return ((value << shift) & 0xFF) | (value >> (8 - shift))

def encrypt_decrypt_file(input_file, output_file, key):
    #Шифрует или дешифрует
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            byte = f_in.read(1)
            if not byte:
                break
            byte_value = byte[0]
            shifted_value = cyclic_shift(byte_value, 2)  # Циклический сдвиг на 2 бита
            encrypted_byte = shifted_value ^ key  # Шифрование/дешифрование
            f_out.write(bytes([encrypted_byte]))  # Записываем зашифрованный байт

# Получение данных от пользователя
user_input = input("Введите данные для сохранения в файл: ")

# Сохранение введенных данных в файл
with open('resourse/input.bin', 'wb') as f:
    f.write(user_input.encode('utf-8'))

# Получение ключа от пользователя
key = int(input("Введите ключ (целое число от 0 до 255): "))
key = key & 0xFF

# Шифрование
encrypt_decrypt_file('resourse/input.bin', 'resourse/output.bin', key)
print("Файл зашифрован и сохранен как 'output.bin'.")

# Дешифрование
encrypt_decrypt_file('resourse/output.bin', 'resourse/decrypted.bin', key)
print("Файл расшифрован и сохранен как 'decrypted.bin'.")
