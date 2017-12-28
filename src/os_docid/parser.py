import hashlib
from docid import DocID


_DOMAINID_LENGTH = 8
_SITEID_LENGTH = 8
_URLID_LENGTH = 16
_HEX_DOMAINID_LENGTH = _DOMAINID_LENGTH * 2
_HEX_SITEID_LENGTH = _SITEID_LENGTH * 2
_HEX_URLID_LENGTH = _URLID_LENGTH * 2
_HEX_HOSTID_LENGTH = _HEX_DOMAINID_LENGTH + _HEX_SITEID_LENGTH
_HEX_DOCID_LENGTH = _HEX_HOSTID_LENGTH + _HEX_URLID_LENGTH
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


def _docid_from_string_parts(domainid, siteid, urlid):
    return DocID(domainid.decode('hex'), siteid.decode('hex'), urlid.deocde('hex'))


def _docid_from_url(url, start_index):
    domain, site = _parse_url(url, start_index)
    domainid = hashlib.md5(domain).digest()[0:_DOMAINID_LENGTH]
    siteid = hashlib.md5(site).digest()[0:_SITEID_LENGTH]
    urlid = hashlib.md5(url).digest()
    return DocID(domainid, siteid, urlid)


def _parse_url(url, start_index=0):
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


def parse(data):
    assert isinstance(data, basestring)
    idx = 0
    for c in data:
        if c not in _HEX or (c == '-' and (idx != _HEX_DOMAINID_LENGTH
                                           and idx != _HEX_HOSTID_LENGTH + 1)):
            return _docid_from_url(data, idx)
        idx += 1
        if idx > _HEX_DOCID_LENGTH + 2:
            break
    if idx == _HEX_DOCID_LENGTH:
        return _docid_from_string_parts(data[0:_HEX_DOMAINID_LENGTH],
                                        data[_HEX_DOMAINID_LENGTH:_HEX_HOSTID_LENGTH],
                                        data[_HEX_HOSTID_LENGTH:])
    elif idx == _HEX_DOCID_LENGTH + 2 \
            and data[_HEX_DOCID_LENGTH] == '-' \
            and data[_HEX_HOSTID_LENGTH + 1] == '-':
        return _docid_from_string_parts(data[0:_HEX_DOMAINID_LENGTH],
                                        data[_HEX_DOMAINID_LENGTH +
                                             1:_HEX_HOSTID_LENGTH + 1],
                                        data[_HEX_HOSTID_LENGTH + 2:])
    else:
        raise ValueError('Not docid or url')
