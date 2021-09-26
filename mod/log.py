from datetime import datetime
import os

# Путь до настоящего скрипта
scripDirAbs = os.path.abspath(os.path.dirname(__file__))
pathcd = str(os.path.split(scripDirAbs)[0])  # путь на каталог ниже
dirlog = (os.path.join(pathcd, 'log'))       # объеденение путей


class LogFile:
    """
    Класс логгера, иницируется по умолчанию flog = LogFile()
    Предполагает, что существует папка log на каталог выше
    Допонительные параменты:
        file_log = 'Mylog'   название файла
        cat      = '/log'    путь до каталога с логами
        dateFile = 0         Не добавлять в название файла дату
        printLog = 1         Доплнительно выводить логи в консль
    Запись flog('text')
    """
    def __init__(self,
                 cat: str = dirlog,
                 file_log: str = 'log.txt',
                 dateFile: bool = 1,
                 printLog: bool = 0) -> None:
        self.printLog = printLog
        self.cat = cat
        self.file_log = file_log
        if dateFile:
            self.full_file_name = os.path.join(self.cat,
                                               (datetime.now()).
                                               strftime("%d-%m-%Y" +
                                                        self.file_log))
        else:
            self.full_file_name = os.path.join(self.cat, self.file_log)

    def writer(self, string: str) -> None:
        try:
            linestr = str(string)+'\n'
            self.obj_log = open(self.full_file_name, 'a')
            self.obj_log.write(linestr)
            if self.printLog:
                print(linestr)
        except IOError:
            print("msg Error!")
        finally:
            self.obj_log.close()

    def __call__(self, string: str) -> None:
        self.writer(string)

    def re(self):  # Стереть содиржимое файла
        f = open(self.full_file_name, 'w')
        f.close()
