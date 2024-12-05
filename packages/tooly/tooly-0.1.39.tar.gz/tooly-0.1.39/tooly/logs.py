import datetime
import logging
import time
from logging.handlers import TimedRotatingFileHandler


class __MyFormatter(logging.Formatter):
    converter = datetime.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        t = ct.strftime("%Y-%m-%d %H:%M:%S")
        s = "%s.%03d" % (t, record.msecs)
        return s


def initLog(fname: str = None,
            enableConsole=True,
            level=logging.DEBUG,
            fileRotateIntervalHour=24,
            fileRotateBackupCnt=1,
            fmt: str = "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s"):
    """
    logging的初始化函数。
    :param fname: 日志文件的名称，如果为空则不记录日志到文件
    :param enableConsole: 是否开启控制台日志输出
    :param level: 日志级别
    :param fileRotateIntervalHour: 日志文件多久滚动一次
    :param fileRotateBackupCnt: 日志文件最大的保存数
    :param fmt: 日志的记录格式
    :return:
    """
    formatter = __MyFormatter(fmt=fmt)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(level)
    streamHandler.setFormatter(formatter)

    time_rotate_file = TimedRotatingFileHandler(filename=fname,
                                                when='S',
                                                interval=3600 * fileRotateIntervalHour,
                                                backupCount=fileRotateBackupCnt)
    time_rotate_file.setFormatter(formatter)
    time_rotate_file.setLevel(level)

    handlers = []
    if fname:
        handlers.append(time_rotate_file)
    if enableConsole:
        handlers.append(streamHandler)

    if handlers:
        logging.basicConfig(level=level, handlers=handlers)


if __name__ == '__main__':
    initLog("a.log")
    for i in range(10):
        msg = f"hello:{i}"
        logging.debug(msg)
        time.sleep(1)
