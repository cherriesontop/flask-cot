import time


def day_id(epoch=None):
    if epoch is None:
        epoch = time.time()
    return int(epoch // 86400)


def week_id(epoch=None):
    if epoch is None:
        epoch = time.time()
    return int(epoch // 604800)


def month_id(epoch=None):
    if epoch is None:
        epoch = time.time()
    t = time.gmtime(epoch)
    return int((t.tm_year * 12) + t.tm_mon)


def year_id(epoch=None):
    if epoch is None:
        epoch = time.time()
    t = time.gmtime(epoch)
    return int(t.tm_year)
