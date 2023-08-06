import re

def lxml_to_dict(element):
    ret = {}
    if len(list(element)) == 0:
        tag = re.sub(r'{.*}', '', element.tag)
        ret[tag] = element.text
    else:
        count = {}
        for elem in element:
            subdict = lxml_to_dict(elem)
            tag = re.sub(r'{.*}', '', element.tag)
            subtag = re.sub(r'{.*}', '', elem.tag)
            if subtag in ret.get(tag, {}):
                count[subtag] = count.get(subtag, 0) + 1
                elemtag = subtag + str(count[subtag])
                subdict = {elemtag: subdict[subtag]}
            if tag in ret:
                ret[tag].update(subdict)
            else:
                ret[tag] = subdict
    return ret