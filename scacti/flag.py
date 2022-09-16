import re


def check_int(string):
    return re.match(r"[-+]?\d+(\.0*)?$", string) is not None


def processFlags(rawflag):
    number = []
    letter = []
    switchflag = ("e", "u", "W")
    switchflags = "euW"
    dictflag = {"e": 0.0, "u": 0.0, "W": 0.0}
    flag = re.findall("(\d+|[A-Za-z]+)", rawflag)
    for item in flag:
        # print(type(item))
        if check_int(item) == True:
            number.append(float(item))
        else:
            if item.startswith(switchflag) == True:
                dictflag.update({item[0]: 1.0})
            for w in switchflags:
                item = item.replace(w, "")
            letter.append(item)
    dictflag.update(dict(zip(letter, number)))
    return dictflag


# print(processFlags("eWMt100Mb60"))
