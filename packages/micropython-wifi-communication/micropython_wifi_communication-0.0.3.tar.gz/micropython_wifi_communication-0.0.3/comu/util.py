def validator(item):
    item = item.split('0: 0}')
    item = item[len(item) - 2] + '0: 0}'
    try:
        item = eval(item)
    except:
        return True, False
    x = False
    y = False
    try:
        item[1]
    except:
        x = True
    try:
        item[0]
    except:
        y = True
    if x or y:
        return True, False
    return False, item