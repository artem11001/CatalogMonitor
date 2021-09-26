import hashlib
import os
from sys import argv, exc_info
from mod.log import LogFile
from mod.argv import argv
import shelve
from datetime import datetime


checkdir = {}
savedict = {}

logger = LogFile(printLog=1)


def log_notify(editlist):
    """
    Логгирует изменения в каталоге мониторинга
    """
    log = LogFile(printLog=1, file_log='log_notify')
    for line in editlist:
        log(line)


def smtp_notify():
    pass


group_to_fuction_notify = {
    """
    Словарь функций уведомлений, smtp пока что нет.
    """
    "smtp": smtp_notify,
    "log": log_notify
    }


def md5sum(filename):
    """
    Хеш-сумма файла
    """
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def revTree(dirname: str, ignortDir: list, ignoreExt: list):
    """
    Обхода каталога с учетом фильтров игора
    """
    for (thisDir, subsHere, filesHere) in os.walk(dirname):
        basename = os.path.basename(thisDir)
        if basename in ignortDir:            # фильтр игнорируемых каталогов
            continue
        if os.path.islink(basename):         # игнорирование ссылок
            continue
        thisDir = os.path.normpath(thisDir)  # нормализация пути
        fixname = os.path.normcase(thisDir)  # Нормализовать регистр имени пути

        if fixname in checkdir:              # сканировался ли путь раньше
            continue
        else:
            checkdir[fixname] = {}
            for filename in filesHere:
                ext = os.path.splitext(filename)[1]
                if ext in ignoreExt:         # фильтр игнорируемых расширений
                    continue
                fullname = os.path.join(os.path.abspath(thisDir), filename)
                try:
                    size = os.path.getsize(fullname)      # размер файла
                    hexsum = md5sum(fullname)             # хеш-сумма
                    filtime = datetime.fromtimestamp(     # дата изменения
                        os.path.getmtime(fullname)).strftime('%Y-%m-%d %H:%M')
                except Exception:
                    logger('error', exc_info()[0])
                else:
                    savedict[fullname] = {"size": size, "hexsum": hexsum,
                                          "filtime": filtime}


def dumpBaseShelv(dirBaseShelve: str):
    """
    Копирование базы данных, удаление настоящий.
    """
    dumpBaseName = dirBaseShelve + datetime.now().strftime("%Y-%m-%d %H:%M")
    fileFrom = open(dirBaseShelve, 'rb')
    fileTo = open(dumpBaseName, 'wb')
    while True:
        bytesFrom = fileFrom.read(1024)
        if not bytesFrom:
            break
        fileTo.write(bytesFrom)
    os.remove(dirBaseShelve)


def main(recursionError: int = 0):
    dictArgv = argv()
    editlist = []                # список изменений в каталоге

    if recursionError > 5:       # Если какая-то рекурсия, то выход
        logger('recursionError')
        os._exit(1)

    if not os.path.isdir(dictArgv['monitorDir']):
        raise NameError('not dir %s' % dictArgv['monitorDir'])
    revTree(dictArgv['monitorDir'], dictArgv['ignortDir'],
            dictArgv['ignoreExt'])
    baseshelv = shelve.open(dictArgv['dirBaseShelve'])
    for name, value in savedict.items():
        if name not in baseshelv:
            baseshelv[name] = value
            logger(f'{datetime.now().strftime("%d-%m-%Y")}\
    add name = {name} vale {value}')
        else:
            baseValues = baseshelv[name]
            for item, val in value.items():
                if baseValues[item] != val:
                    editlist.append(f'{datetime.now().strftime("%d-%m-%Y")}\
    file {name} changed {item} = {baseValues[item]} != {val}')

    if editlist:
        recursionError += 1
        dumpBaseShelv(dictArgv['dirBaseShelve'])
        group_to_fuction_notify[dictArgv['logging']](editlist)
        del editlist                 # очистить массив, иначе рекурсия
        return main(recursionError)  # Создание новой базы с измененниями

    if not recursionError:
        logger("%s Scanning dir =%s no change" %
               (datetime.now().strftime("%d-%m-%Y"), dictArgv['monitorDir']))


main()
