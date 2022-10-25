from genericpath import exists
import sys
import datetime
import time
import os


def log(msg, level: str = 'info', where: str = None) -> None:
    '''Print message'''
    levelmsg = level if level else "null"
    mainmsg = f'[{str(datetime.datetime.now())}][{where if where else (lambda f: f.f_locals["c_logger_where"] if "c_logger_where" in f.f_locals else f.f_code.co_name)(sys._getframe().f_back)}/{levelmsg}] {str(msg if msg is not None else "(null)")}'
    colorlevel = levelmsg.lower()
    if colorlevel.endswith('info'):
        print("\033[1;37;40m%s\033[0m" % mainmsg)
    elif colorlevel.endswith('warn'):
        print("\033[1;33;40m%s\033[0m" % mainmsg)
    elif colorlevel.endswith('error'):
        print("\033[1;31;40m%s\033[0m" % mainmsg)
    else:
        print(mainmsg)

def unixtime() -> int:
    return round(time.mktime(datetime.datetime.now().timetuple()) * 1000)

def fread(path:str,encoding="utf-8"):
    if exists(path):
        with open(path,"r",encoding=encoding) as fs:
            return fs.read()
    else:
        log("file not found",'error')
        return None
    
def fwrite(path:str,content:str,encoding='utf-8'):
    with open(path,'w',encoding=encoding) as fs:
        fs.write(content)

def listdir(dir: str, includeFiles=True, includeDirectories=False):
    for root, dirs, files in os.walk(dir):
        if includeDirectories:
            for child in dirs:
                p = os.path.join(root, child)
                yield p
        if includeFiles:
            for child in files:
                p = os.path.join(root, child)
                yield p
