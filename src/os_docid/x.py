"""Generate DocID from URL.

This file can be used alone.
"""

import binascii
import hashlib
from collections import namedtuple

_DOMAINID_LENGTH = 16
_SITEID_LENGTH = 16
_URLID_LENGTH = 32
_HOSTID_LENGTH = _DOMAINID_LENGTH + _SITEID_LENGTH
_DOCID_LENGTH = _HOSTID_LENGTH + _URLID_LENGTH
_READABLE_DOCID_LENGTH = _DOCID_LENGTH + 2

_BYTE_DOMAINID_LENGTH = _DOMAINID_LENGTH // 2
_BYTE_SITEID_LENGTH = _SITEID_LENGTH // 2
_BYTE_URLID_LENGTH = _URLID_LENGTH // 2

_HEX = set([i for i in b"0123456789abcdefABCDEF"])

_SYM_MINUS = b"-"[0]
_SYM_SLASH = b"/"[0]
_SYM_DOT = b"."[0]
_SYM_COLON = b":"[0]

_SECOND_DOMAIN_SET = set(
    [
        "ha",
        "hb",
        "ac",
        "sc",
        "gd",
        "sd",
        "he",
        "ah",
        "qh",
        "sh",
        "hi",
        "bj",
        "fj",
        "tj",
        "xj",
        "zj",
        "hk",
        "hl",
        "jl",
        "nm",
        "hn",
        "ln",
        "sn",
        "yn",
        "co",
        "mo",
        "cq",
        "gs",
        "js",
        "tw",
        "gx",
        "jx",
        "nx",
        "sx",
        "gz",
        "xz",
        "cat",
        "edu",
        "net",
        "biz",
        "mil",
        "int",
        "com",
        "gov",
        "org",
        "pro",
        "name",
        "aero",
        "info",
        "coop",
        "jobs",
        "mobi",
        "arpa",
        "travel",
        "museum",
    ]
)

_SECOND_DOMAIN_SET = set([_i.encode() for _i in _SECOND_DOMAIN_SET])

_TOP_DOMAIN_SET = set(
    [
        "ac",
        "co",
        "cat",
        "edu",
        "net",
        "biz",
        "mil",
        "int",
        "com",
        "gov",
        "org",
        "pro",
        "name",
        "aero",
        "info",
        "coop",
        "jobs",
        "mobi",
        "arpa",
        "travel",
        "museum",
    ]
)


_TOP_DOMAIN_SET = set([_i.encode() for _i in _TOP_DOMAIN_SET])


class DocID(namedtuple("DocID", "d_bytes, s_bytes, u_bytes")):
    """DocID.

    Attributes:
        d_bytes (bytes): Domain id bytes.
        s_bytes (bytes): Site id bytes.
        u_bytes (bytes): URL id bytes.

    """

    __slots__ = ()

    @property
    def bytes(self):
        return b"".join(self)

    def hexlify(self, sep=b""):
        return sep.join(binascii.hexlify(_i) for _i in self)

    def __str__(self):
        return self.hexlify(sep=b"-").decode()

    __repr__ = __str__


def _docid_frox_hex(domainid, siteid, urlid):
    return DocID(
        binascii.a2b_hex(domainid), binascii.a2b_hex(siteid), binascii.a2b_hex(urlid)
    )


def _digest(obj):
    return hashlib.md5(obj).digest()


class Parser(object):
    def parse(self, data, start_idx=0):
        raise NotImplementedError("Not supported data format")


class UrlParser(Parser):
    def __init__(self):
        self._last_site = None
        self._last_site_length = -1
        self._last_siteid = None
        self._last_domainid = None

    def parse(self, url, start_idx=0):
        if (
            self._last_site
            and url.startswith(self._last_site)
            and len(url) > self._last_site_length
            and url[self._last_site_length] == _SYM_SLASH
        ):
            pass
        else:
            domain, self._last_site = self._parse_url(url, start_idx)
            self._last_site_length = len(self._last_site)
            self._last_domainid = _digest(domain)[0:_BYTE_DOMAINID_LENGTH]
            self._last_siteid = _digest(self._last_site)[0:_BYTE_SITEID_LENGTH]
        urlid = _digest(url)
        return DocID(self._last_domainid, self._last_siteid, urlid)

    def _parse_url(self, url, start_index=0):
        url_length = len(url)
        host_head = host_tail = 0
        domain_head = domain_tail = domain_pre_head = domain_post_head = -1
        find_domain = deal_domain = False

        _i = start_index
        while _i < url_length:
            _c = url[_i]
            if _c == _SYM_DOT:
                deal_domain = True
            elif _c == _SYM_SLASH:
                break
            elif _c == _SYM_COLON:
                if (
                    _i + 2 < url_length
                    and url[_i + 1] == _SYM_SLASH
                    and url[_i + 2] == _SYM_SLASH
                ):
                    _i += 3
                    domain_head = domain_pre_head = domain_post_head = domain_tail = _i
                    continue
                elif not find_domain:
                    deal_domain = True
                    find_domain = True
            if deal_domain:
                domain_pre_head, domain_head = domain_head, domain_post_head
                domain_post_head, domain_tail = domain_tail, _i
                deal_domain = False
            _i += 1
        host_tail = _i
        if not find_domain:
            domain_pre_head, domain_head = domain_head, domain_post_head
            domain_post_head, domain_tail = domain_tail, _i
        if (
            url[domain_head + 1 : domain_post_head] in _SECOND_DOMAIN_SET
            and not url[domain_post_head + 1 : domain_tail] in _TOP_DOMAIN_SET
        ):
            domain_head = domain_pre_head

        while url[domain_head] == _SYM_DOT:
            domain_head += 1
        return url[domain_head:domain_tail], url[host_head:host_tail]


class DocIDParser(Parser):
    def parse(self, data, start_idx=0):
        return _docid_frox_hex(
            data[0:_DOMAINID_LENGTH],
            data[_DOMAINID_LENGTH:_HOSTID_LENGTH],
            data[_HOSTID_LENGTH:],
        )


class ReadableDocIDParser(Parser):
    def parse(self, data, start_idx=0):
        return _docid_frox_hex(
            data[0:_DOMAINID_LENGTH],
            data[_DOMAINID_LENGTH + 1 : _HOSTID_LENGTH + 1],
            data[_HOSTID_LENGTH + 2 :],
        )


_PARSER = Parser()
_URL_PARSER = UrlParser()
_DOCID_PARSER = DocIDParser()
_R_DOCID_PARSER = ReadableDocIDParser()


def docid(url, encoding="ascii"):
    """Get DocID from URL.

    DocID generation depends on bytes of the URL string.
    So, if non-ascii charactors in the URL, encoding should
    be considered properly.

    Args:
        url (str or bytes): Pre-encoded bytes or string will be encoded with the
            'encoding' argument.
        encoding (str, optional): Defaults to 'ascii'. Used to encode url argument
            if it is not pre-encoded into bytes.

    Returns:
        DocID: The DocID object.

    Examples:

        >>> from os_docid import docid

        >>> docid('http://www.google.com/')
        1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd

        >>> docid('1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd')
        1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd

        >>> docid('1d5920f4b44b27a8ed646a3334ca891fff90821feeb2b02a33a6f9fc8e5f3fcd')
        1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd

        >>> docid('abc')  
        NotImplementedError: Not supported data format

    """

    if not isinstance(url, bytes):
        url = url.encode(encoding)

    parser = _URL_PARSER
    idx = 0
    for _c in url:
        if _c not in _HEX:
            if not (
                _c == _SYM_MINUS
                and (idx == _DOMAINID_LENGTH or idx == _HOSTID_LENGTH + 1)
            ):
                return parser.parse(url, idx)
        idx += 1
        if idx > 4:
            break
    _l = len(url)
    if _l == _DOCID_LENGTH:
        parser = _DOCID_PARSER
    elif (
        _l == _READABLE_DOCID_LENGTH
        and url[_DOMAINID_LENGTH] == _SYM_MINUS
        and url[_HOSTID_LENGTH + 1] == _SYM_MINUS
    ):
        parser = _R_DOCID_PARSER
    else:
        parser = _PARSER

    return parser.parse(url, idx)


if __name__ == "__main__":
    url = "http://www.google.com/"
    print(docid(url))
