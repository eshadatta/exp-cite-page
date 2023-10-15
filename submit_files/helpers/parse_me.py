from datetime import datetime
def parse_dict(d, doc, t, xml_docs  =[]):
    print(doc.keys())
    for k, v in d.items():
        if isinstance(v, dict):
            parse_dict(d[k], doc, t)
        else:
            if k == 'month':
                d[k] = t.strftime("%m")
            elif k == 'day':
                d[k] = t.strftime("%d")
            elif k == 'year':
                d[k] = t.strftime("%Y")
            elif k in list(doc.keys()):
                d[k] = doc[k]
    return d
