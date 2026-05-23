def read_uint16(file):
    return int.from_bytes(file.read(2), byteorder='little')


def read_uint32(file):
    return int.from_bytes(file.read(4), byteorder='little')


def read_uint64(file):
    return int.from_bytes(file.read(8), byteorder='little')


def read_int16(file):
    return int.from_bytes(file.read(2), byteorder='little', signed=True)


def parse_binary_file(file_path):
    with open(file_path, 'rb') as f:
        signature = f.read(4)
        if signature != b'DATA':
            raise ValueError("Неверная сигнатура файла.")

        version = read_uint16(f)

        record_count = read_uint32(f)

        total_temperature = 0
        active_flags_count = 0

        for _ in range(record_count):
            timestamp = read_uint64(f)
            id_ = read_uint32(f)
            temperature = read_int16(f)
            state_flag = ord(f.read(1))

            temperature_celsius = temperature / 100.0

            total_temperature += temperature_celsius
            active_flags_count += bin(state_flag).count('1')

        average_temperature = total_temperature / record_count if record_count > 0 else 0

        print(f"Версия: {version}. Количество записей: {record_count}.")
        print(f"Средняя температура: {average_temperature:.2f} °C")
        print(f"Количество активных флагов: {active_flags_count}")

if __name__ == "__main__":
    file_path = "resourse/data.bin"
    parse_binary_file(file_path)
