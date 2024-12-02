import argparse
import json

class Assembler:
    def __init__(self, path_to_code_file, path_to_binary_file, path_to_log_file):
        self.path_binary = path_to_binary_file
        self.path_code = path_to_code_file
        self.path_log = path_to_log_file
        self.bytes = []
        self.log_data = []

    def assemble(self):
        with open(self.path_code, 'rt') as code:
            for line in code:
                line = line.split('\n')[0].strip()
                if not line: continue
                command, *args = line.split()
                match command:
                    case "LOAD":
                        if len(args) != 3:
                            raise SyntaxError(f"{line}\nУ операции \"Загрузка константы\" должно быть 3 аргумента")
                        self.bytes.append(self.load(int(args[0]), int(args[1]), int(args[2])))
                    case "READ":
                        if len(args) != 4:
                            raise SyntaxError(f"{line}\nУ операции \"Чтение значения из памяти\" должно быть 4 аргумента")
                        self.bytes.append(self.read(int(args[0]), int(args[1]), int(args[2]), int(args[3])))
                    case "WRITE":
                        if len(args) != 3:
                            raise SyntaxError(f"{line}\nУ операции \"Запись значения в память\" должно быть 3 аргумента")
                        self.bytes.append(self.write(int(args[0]), int(args[1]), int(args[2])))
                    case "SQRT":
                        if len(args) != 4:
                            raise SyntaxError(f"{line}\nУ операции \"Унарная операция: sqrt()\" должно быть 4 аргумента")
                        self.bytes.append(self.sqrt(int(args[0]), int(args[1]), int(args[2]), int(args[3])))
                    case _:
                        raise SyntaxError(f"{line}\nНеизвестная операция")
        with open(self.path_binary, 'wb') as binary:
            for byte in self.bytes:
                binary.write(byte)

        # Сохранение логов в формате JSON
        if self.path_log:
            with open(self.path_log, 'w', encoding="utf-8") as log_file:
                json.dump(self.log_data, log_file, ensure_ascii=False, indent=4)


    def load(self, A, B, C):
        if A != 27: raise ValueError("Параметр А должен быть равен 27")
        if not (0 <= B < (1 << 4)): raise ValueError("Адрес B должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= C < (1 << 22)): raise ValueError("Константа C должна быть в пределах от 0 до 4194303 (2^22-1)")
        bits = (C << 9) | (B << 5) | A
        bits = bits.to_bytes(7, byteorder="little")
        # Логирование операции
        self.log_data.append({
            "command": "LOAD",
            "A": A,
            "B": B,
            "C": C,
            "binary": bits.hex()
        })
        return bits

    def read(self, A, B, C, D):
        if A != 3: raise ValueError("Параметр А должен быть равен 3")
        if not (0 <= B < (1 << 4)): raise ValueError("Адрес B должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= C < (1 << 4)): raise ValueError("Адрес C должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= D < (1 << 9)): raise ValueError("Адрес D должен быть в пределах от 0 до 511 (2^9-1)")
        bits = (D << 13) | (C << 9) | (B << 5) | A
        bits = bits.to_bytes(7, byteorder="little")
        # Логирование операции
        self.log_data.append({
            "command": "READ",
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "binary": bits.hex()
        })
        return bits

    def write(self, A, B, C):
        if A != 11: raise ValueError("Параметр А должен быть равен 11")
        if not (0 <= B < (1 << 4)): raise ValueError("Адрес B должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= C < (1 << 31)): raise ValueError("Адрес C должен быть в пределах от 0 до 2147483647 (2^31-1)")
        bits = (C << 9) | (B << 5) | A
        bits = bits.to_bytes(7, byteorder="little")
        # Логирование операции
        self.log_data.append({
            "command": "WRITE",
            "A": A,
            "B": B,
            "C": C,
            "binary": bits.hex()
        })
        return bits

    def sqrt(self, A, B, C, D):
        if A != 19: raise ValueError("Параметр А должен быть равен 19")
        if not (0 <= B < (1 << 4)): raise ValueError("Адрес B должен быть в пределах от 0 до 15 (2^4-1)")
        if not (0 <= C < (1 << 31)): raise ValueError("Адрес C должен быть в пределах от 0 до 2147483647 (2^31-1)")
        if not (0 <= D < (1 << 9)): raise ValueError("Адрес D должен быть в пределах от 0 до 511 (2^9-1)")
        bits = (D << 40) | (C << 9) | (B << 5) | A
        bits = bits.to_bytes(7, byteorder="little")
        # Логирование операции
        self.log_data.append({
            "command": "SQRT",
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "binary": bits.hex()
        })
        return bits


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("asm_file", help="Входной файл (*.asm)")
    parser.add_argument("bin_file", help="Выходной файл (*.bin)")
    parser.add_argument("-l", "--log_file", help="Лог файл (*.json)")
    args = parser.parse_args()
    assembler = Assembler(args.asm_file, args.bin_file, args.log_file)
    try:
        assembler.assemble()
        print(f"Ассемблирование выполнено успешно. Выходной файл: {args.bin_file}")
    except ValueError as error:
        print(f"Ошибка:\n{error}")