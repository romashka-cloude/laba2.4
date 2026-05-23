def process_file(input_file, output_file):
    denominator = (73 ** 2 + 29)

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            numbers = line.split()
            for num_str in numbers:
                try:
                    number = int(num_str)
                    if number % 7 == 0:
                        result = number * 100 / denominator
                        outfile.write(f"{result}\n")
                except ValueError:
                    continue

if __name__ == "__main__":
    input_filename = 'resourse/text.txt'
    output_filename = 'resourse/output.txt'

    process_file(input_filename, output_filename)
    print(f"Обработка завершена. Результаты записаны в '{output_filename}'.")
