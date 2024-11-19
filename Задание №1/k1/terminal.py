from zipfile import ZipFile
from window_mode import Window
import time


class MyTerminal:
    def __init__(self, user_name, comp_name, zip_path, start_path, file_system : ZipFile):
        self.start_time = time.time()
        self.user_name = user_name
        self.comp_name = comp_name
        self.zip_path = zip_path
        self.start_path = start_path
        self.fs = file_system
        self.cur_d = ''
        self.cur_d_true = f'{zip_path[:zip_path.find(".zip")]}/'
        self.polling = False
        self.window = None

    def attach(self, window: Window):
        self.window = window
        self.window.write(f'{self.user_name}@{self.comp_name}:~{self.cur_d}$ ')

    def output(self, message, end='\n'):
        self.window.write(message + end)


    def command_dispatcher(self, command):
        self.output(command)
        params = command.split()
        if params[0] == 'exit':
            self.window.stop_polling()
            return
        elif params[0] == 'cd':
            temp_dir = self.cd(params[1:])
            if temp_dir is not None:
                self.cur_d_true = temp_dir
                self.cur_d = temp_dir[5:]
        elif params[0] == 'ls':
            self.ls(params[1:])
        elif params[0] == 'uptime':
            self.output(self.uptime())
        elif params[0] == 'find':
            self.find(params[1:])
        elif params[0] == 'test':
            self.test()
        else:
            self.output("Команда не найдена")
        self.window.write(f'{self.user_name}@{self.comp_name}:~{self.cur_d}$ ')

    def cd(self, params):
        if len(params) == 0:
            return ''

        directory = params[-1]

        directory = directory.strip('/')
        directory = directory.split('/')

        new_directory = self.cur_d_true[:-1].split('/')
        if new_directory == ['']:
            new_directory = []
        for i in directory:
            if i == '..':
                if self.cur_d != '':
                    if len(new_directory) > 0:
                        new_directory.pop()
                    else:
                        self.output('Некорректный путь до директории')
                        return
                else:
                    self.output('Некорректный путь до директории')
                    return
            else:
                new_directory.append(i)

        new_path = '/'.join(new_directory) + '/'
        if new_path == '/':
            return ''

        for file in self.fs.namelist():
            if file.startswith(new_path):
                return new_path
        self.output('Директория с таким названием отсутствует')
        return


    def ls(self, params):
        work_directory = self.cur_d_true
        if len(params) > 0:
            work_directory = self.cd([params[-1]])
            if work_directory is None:
                return ''

        files = set()
        for file in self.fs.namelist():
            if file.startswith(work_directory):
                ls_name = file[len(work_directory):]
                if '/' in ls_name:
                    ls_name = ls_name[:ls_name.index('/')]
                files.add(ls_name)
        self.output('\n'.join(sorted(filter(lambda x: len(x) > 0, files))))
        return '\n'.join(sorted(filter(lambda x: len(x) > 0, files)))


    def uptime(self):
        cur_time = time.time()
        res_time = str(int(cur_time - self.start_time)//60+1)
        return "up " + res_time + " min"


    def find(self, params):
        if len(params) > 0:
            find = params[-1]
            files = []

            # Получаем список файлов в текущем каталоге
            current_files = self.fs.namelist()

            # Поиск файлов, содержащих 'find' в названии
            for file in current_files:
                if find in file:
                    files.append(file[5:])  # Убираем префикс из пути

            if len(files) == 0:
                self.output("Файл не найден")
                return "Файл не найден"
            else:
                result = '\n'.join(files)
                self.output(result)
                return result
        else:
            self.output("Параметры не были переданы")
            return "Параметры не были переданы"