import os

absDir = os.path.abspath(os.path.dirname(__file__))
pathcd = str(os.path.split(absDir)[0])
dirbaseShelv = (os.path.join(pathcd, 'log/baseshelv'))

dirBaseShelve = dirbaseShelv           # каталог для базы shelv
monitorDir = pathcd            # каталог монитора
ignortDir = "__pycache__ log"  # игнорируемые каталоги
ignoreExt = ".pyc .log'"       # игнорируемые расширения
