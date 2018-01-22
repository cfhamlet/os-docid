import binascii


class DocID(object):
    def __init__(self, b_domainid, siteid, b_urlid):
        self._b_parts = (b_domainid, siteid, b_urlid)

    def __str__(self):
        return '-'.join([binascii.hexlify(i) for i in self._b_parts])