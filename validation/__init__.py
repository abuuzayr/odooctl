class Base(object):
        pass


class ExceptionBase(Exception):
        pass


def check_true(target, msg):
    if not target:
        raise ExceptionBase(msg)
