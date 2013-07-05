import collections

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
