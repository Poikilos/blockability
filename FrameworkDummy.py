
def IndexOf(val, sub, start=0, end=-1):
    if end<0:
        end=len(val)
    result = -1
    return val.find(sub, start, end)

def Substring(val, start, count=-1):
    if count<0:
        count = len(val)-start
    end = start + count
    return val[start:end]

def StartsWith(haystack, needle):
    result = False
    if (haystack is not None) and (needle is not None) and (len(needle)>0):
        if haystack[0:len(needle)] == needle:
            result = True
    return result

def EndsWith(haystack, needle):
    result = False
    if (haystack is not None) and (needle is not None) and (len(needle)>0):
        if haystack[:-1*len(needle)] == needle:
            result = True
    return result
