import hashlib

from .docid import DocID

_DOMAINID_LENGTH = 16
_SITEID_LENGTH = 16
_URLID_LENGTH = 32
_HOSTID_LENGTH = _DOMAINID_LENGTH + _SITEID_LENGTH
_DOCID_LENGTH = _HOSTID_LENGTH + _URLID_LENGTH
_READABLE_DOCID_LENGTH = _DOCID_LENGTH + 2

_BYTE_DOMAINID_LENGTH = _DOMAINID_LENGTH // 2
_BYTE_SITEID_LENGTH = _SITEID_LENGTH // 2
_BYTE_URLID_LENGTH = _URLID_LENGTH // 2
_HEX = set([i for i in '0123456789abcdefABCDEF'])

_SECOND_DOMAIN_SET = set([
    "ha", "hb", "ac", "sc", "gd", "sd", "he", "ah", "qh", "sh", "hi",
    "bj", "fj", "tj", "xj", "zj", "hk", "hl", "jl", "nm", "hn", "ln",
    "sn", "yn", "co", "mo", "cq", "gs", "js", "tw", "gx", "jx", "nx",
    "sx", "gz", "xz",
    "cat", "edu", "net", "biz", "mil", "int", "com", "gov", "org", "pro",
    "name", "aero", "info", "coop", "jobs", "mobi", "arpa",
    "travel", "museum",
])

_TOP_DOMAIN_SET = set([
    "ac", "co",
    "cat", "edu", "net", "biz", "mil", "int", "com", "gov", "org", "pro",
    "name", "aero", "info", "coop", "jobs", "mobi", "arpa",
    "travel", "museum",
])


def _docid_from_string_parts(domainid_str, siteid_str, urlid_str):
    return DocID(bytearray.fromhex(domainid_str),
                 bytearray.fromhex(siteid_str),
                 bytearray.fromhex(urlid_str))


class Parser(object):
    def parse(self, data, start_idx=0):
        raise NotImplementedError('Not supported data format')


class UrlParser(Parser):
    def __init__(self):
        self._last_site = None
        self._last_site_length = -1
        self._last_siteid = None
        self._last_domainid = None

    def parse(self, url, start_idx=0):
        if self._last_site and url.startswith(self._last_site) \
                and len(url) > self._last_site_length \
                and url[self._last_site_length] == '/':
            pass
        else:
            domain, self._last_site = self._parse_url(url, start_idx)
            self._last_site_length = len(self._last_site)
            self._last_domainid = hashlib.md5(domain.encode('utf8')).digest()[
                0:_BYTE_DOMAINID_LENGTH]
            self._last_siteid = hashlib.md5(self._last_site.encode('utf8')).digest()[
                0:_BYTE_SITEID_LENGTH]
        urlid = hashlib.md5(url.encode('utf8')).digest()
        return DocID(self._last_domainid, self._last_siteid, urlid)

    def _parse_url(self, url, start_index=0):
        url_length = len(url)
        host_head = host_tail = 0
        domain_head = domain_tail = domain_pre_head = domain_post_head = -1
        find_domain = deal_domain = False

        i = start_index
        while i < url_length:
            c = url[i]
            if c == '.':
                deal_domain = True
            elif c == '/':
                break
            elif c == ':':
                if i + 2 < url_length and url[i + 1] == '/' and url[i + 2] == '/':
                    i += 3
                    domain_head = domain_pre_head = domain_post_head = domain_tail = i
                    continue
                elif not find_domain:
                    deal_domain = True
                    find_domain = True
            if deal_domain:
                domain_pre_head,  domain_head = domain_head, domain_post_head
                domain_post_head, domain_tail = domain_tail, i
                deal_domain = False
            i += 1
        host_tail = i
        if not find_domain:
            domain_pre_head, domain_head = domain_head, domain_post_head
            domain_post_head, domain_tail = domain_tail, i
        if url[domain_head + 1:domain_post_head] in _SECOND_DOMAIN_SET \
                and not url[domain_post_head + 1:domain_tail] in _TOP_DOMAIN_SET:
            domain_head = domain_pre_head

        domain_head += 1
        return url[domain_head: domain_tail], url[host_head:host_tail]


class DocIDParser(Parser):
    def parse(self, data, start_idx=0):
        return _docid_from_string_parts(data[0:_DOMAINID_LENGTH],
                                        data[_DOMAINID_LENGTH:_HOSTID_LENGTH],
                                        data[_HOSTID_LENGTH:])


class ReadableDocIDParser(Parser):
    def parse(self, data, start_idx=0):
        return _docid_from_string_parts(data[0:_DOMAINID_LENGTH],
                                        data[_DOMAINID_LENGTH +
                                             1:_HOSTID_LENGTH + 1],
                                        data[_HOSTID_LENGTH + 2:])


_PARSER = Parser()
_URL_PARSER = UrlParser()
_DOCID_PARSER = DocIDParser()
_R_DOCID_PARSER = ReadableDocIDParser()


def parse(data):
    parser = _URL_PARSER
    idx = 0
    for c in data:
        if c not in _HEX:
            if not (c == '-' and (idx == _DOMAINID_LENGTH
                                  or idx == _HOSTID_LENGTH + 1)):
                return parser.parse(data, idx)
        idx += 1
        if idx > 4:
            break
    l = len(data)
    if l == _DOCID_LENGTH:
        parser = _DOCID_PARSER
    elif l == _READABLE_DOCID_LENGTH \
            and data[_DOMAINID_LENGTH] == '-' \
            and data[_HOSTID_LENGTH + 1] == '-':
        parser = _R_DOCID_PARSER
    else:
        parser = _PARSER

    return parser.parse(data, idx)
