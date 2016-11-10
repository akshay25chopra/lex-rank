from sys import version_info


PY3 = version_info[0] == 3

if PY3:
    bytes = bytes
    unicode = str
else:
    bytes = str
    unicode = unicode


def to_unicode(object):
    if isinstance(object, unicode):
        return object
    elif isinstance(object, bytes):
        return object.decode("utf8")