import argparse
import json


class Interpreter:
    def __init__(self, path_to_binary_file, path_to_result_file, boundaries):
        self.path_result = path_to_result_file
        self.boundaries = list(map(int, boundaries.split(':')))
        self.registers = [0] * (self.boundaries[1] - self.boundaries[0] + 1)
        with open(path_to_binary_file, 'rb') as binary_file:
            self.byte_code = int.from_bytes(binary_file.read(), byteorder="little")

    def interpret(self):
        while self.byte_code != 0:
            A = self.byte_code & ((1 << 5) - 1)
            self.byte_code >>= 5
            match A:
                case 27: self.load()
                case 3: self.read()
                case 11: self.write()
                case 19: self.sqrt()
                case _: raise ValueError("В бинарном файле содержатся невалидные данные: неверный байт-код")
        # Составляем данные для сохранения в JSON
        result_data = []
        for pos, register in enumerate(self.registers, self.boundaries[0]):
            if register != 0:
                result_data.append({
                    "address": pos,
                    "value": register
                })

        # Сохраняем данные в JSON формате
        with open(self.path_result, 'w', encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)

    def load(self):
        B = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        C = self.byte_code & ((1 << 22) - 1); self.byte_code >>= 47
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[B] = C

    def read(self):
        B = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        C = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        D = self.byte_code & ((1 << 9) - 1); self.byte_code >>= 43
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= self.registers[C] + D <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[B] = self.registers[self.registers[C] + D]

    def write(self):
        B = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        C = self.byte_code & ((1 << 31) - 1); self.byte_code >>= 47
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[C] = self.registers[B]

    def sqrt(self):
        B = self.byte_code & ((1 << 4) - 1); self.byte_code >>= 4
        C = self.byte_code & ((1 << 31) - 1); self.byte_code >>= 31
        D = self.byte_code & ((1 << 9) - 1); self.byte_code >>= 16
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= C <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= self.registers[B] + D <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[C] = (self.registers[self.registers[B] + D]) ** 0.5


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bin_file", help="Входной файл (*.bin)")
    parser.add_argument("res_file", help="Выходной файл (*.json)")
    parser.add_argument("boundaries", help="Границы памяти в формате: <левая>:<правая>")
    args = parser.parse_args()
    interpreter = Interpreter(args.bin_file, args.res_file, args.boundaries)
    try:
        interpreter.interpret()
        print(f"Интерпретация выполнена успешно. Результаты сохранены в {args.res_file}")
    except ValueError as error:
        print(f"Ошибка:\n{error}")