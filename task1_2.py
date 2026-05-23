def create_test_binary_file(file_path):
    with open(file_path, 'wb') as f:
        # Записываем сигнатуру
        f.write(b'DATA')

        # Записываем версию
        f.write((1).to_bytes(2, byteorder='little'))

        # Записываем количество записей
        f.write((3).to_bytes(4, byteorder='little'))

        # Записываем записи
        records = [
            (13148730000000000, 1, 2650, 0b00000001),  # timestamp, ID, температура (25.50°C), флаг
            (13148731000000000, 2, 3100, 0b00000011),  # timestamp, ID, температура (30.00°C), флаг
            (13148732000000000, 3, 1600, 0b00000000)  # timestamp, ID, температура (15.00°C), флаг
        ]

        for timestamp, id_, temperature, state_flag in records:
            # Записываем запись в файл
            f.write(timestamp.to_bytes(8, byteorder='little'))
            f.write(id_.to_bytes(4, byteorder='little'))
            f.write(temperature.to_bytes(2, byteorder='little', signed=True))
            f.write(bytes([state_flag]))  # Записываем один байт для состояния флага


# Создаем тестовый бинарный файл
create_test_binary_file("resourse/data.bin")
