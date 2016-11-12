from sys import version_info


PY3 = version_info[0] == 3

if PY3:
    bytes = bytes
    unicode = str
else:
    bytes = str
    unicode = unicode
string_types = (bytes, unicode,)


def to_string(object):
    return to_unicode(object)


def to_unicode(object):
    if isinstance(object, unicode):
        return object
    elif isinstance(object, bytes):
        return object.decode("utf8")


class ItemsCount(object):
    def __init__(self, value):
        self._value = value

    def __call__(self, sequence): # sequence seems like the number of sentences in a document
        if isinstance(self._value, string_types): # check if the user is entering a string - "10%"
            if self._value.endswith("%"):
                total_count = len(sequence)
                percentage = int(self._value[:-1])
                # at least one sentence should be chosen
                count = max(1, total_count*percentage // 100)
                return sequence[:count]
            else:
                return sequence[:int(self._value)]
        elif isinstance(self._value, (int, float)): # else if the user entered either an integer or a float
            return sequence[:int(self._value)]
        else: # if none of the conditions is matching then its an error
            ValueError("Unsuported value of items count '%s'." % self._value)

    def __repr__(self):
        return to_string("<ItemsCount: %r>" % self._value)