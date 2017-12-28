import binascii


class DocID(object):
    def __init__(self, domainid, siteid, urlid):
        self._parts = (domainid, siteid, urlid)

    def __str__(self):
        return '-'.join([binascii.hexlify(i) for i in self._parts])

    @property
    def domainid(self):
        return self._parts[0]

    @property
    def siteid(self):
        return self._parts[1]

    @property
    def urlid(self):
        return self._parts[2]

    @property
    def docid(self):
        return ''.join(self._parts)
