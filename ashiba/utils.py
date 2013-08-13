import yaml
import socket
import collections

def prettyaml(data, lvl=0, indent='  ', prefix=''):
    if isinstance(data, basestring):
        data = yaml.load(data)
    if isinstance(data, dict):
        if len(data) == 1:
            k, v = data.items()[0]
            out_str = '{}^{}:{}'.format(indent * lvl, k, v)
        else:
            out_str = '\n'.join(
                ['{}{}:{}'.format(indent * lvl, k, prettyaml(v, lvl + 1))
                    for k,v in data.items()])
        out_str = '\n' + out_str
    elif isinstance(data, list):
        out_str = ''.join(['\n{}{}'.format(indent * (lvl - 1) ,
            prettyaml(x, lvl, prefix='- ')) for x in data])
    else:
        out_str = "{0}{1}{2}".format(indent, prefix, data)

    return out_str


def get_port(host, port):
    # Logic borrowed from Tornado's bind_sockets

    flags = socket.AI_PASSIVE
    if hasattr(socket, "AI_ADDRCONFIG"):
        flags |= socket.AI_ADDRCONFIG

    while True:
        try:
            res = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0,
                flags)
            af, socktype, proto, cannonname, sockaddr = res[0]

            s = socket.socket(af, socktype, proto)

            s.setblocking(0)
            s.bind(sockaddr)
            s.listen(128)
        except socket.error as e:
            print("Could not assign to port %s (%s)." % (port, e))
            port += 1
            continue
        return port


def autoviv():
    return collections.defaultdict(autoviv)

def autovivify(d):
    if isinstance(d, dict):
        new_d = autoviv()
        new_d.update(d)
        d = new_d
        for k in d:
            d[k] = autovivify(d[k])
    return d

def dict_diff(a, b):
    diffs = {}
    for k in a:
        if k in b and isinstance(a[k], dict) \
                  and isinstance(b[k], dict):
            dd = dict_diff(a[k], b[k])
            if dd:
                diffs[k] = dd
        elif k not in b or a[k] != b[k]:
            diffs[k] = a[k]
    return diffs

def dict_symmetric_diff(a, b):
    diffs = {}
    for k in set(a.keys()) & set(b.keys()):
        if isinstance(a[k], dict) and isinstance(b[k], dict):
            dsd = dict_symmetric_diff(a[k], b[k])
            if dsd:
                diffs[k] = dsd
        elif a[k] != b[k]:
            diffs[k] = a[k]
    for k in set(a.keys()) ^ set(b.keys()):
        diffs[k] = a[k] if k in a else b[k]
    return diffs
