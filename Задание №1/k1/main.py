from zipfile import ZipFile
from sys import argv
from os.path import exists
from window_mode import Window
from terminal import MyTerminal
import csv

def main():
    if len(argv) > 1:
        config_file = argv[1]

    try:
        with open(config_file, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for line in reader:
                if len(line) >= 2:
                    key, value = line[0].strip(), line[1].strip()
                    if key == "username":
                        user_name = value
                    elif key == "compname":
                        computer_name = value
                    elif key == "zippath":
                        zip_path = value
                    elif key == "startpath":
                        start_path = value
            with ZipFile(zip_path, 'a') as file_system:
                Window(MyTerminal(user_name, computer_name, zip_path, start_path, file_system)).start_polling()
    except FileNotFoundError:
        print(f"Файл {config_file} не найден.")


if __name__ == '__main__':
    main()
