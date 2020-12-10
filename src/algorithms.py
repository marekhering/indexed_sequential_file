
def bisection(key, key_list, first_lower=False):

    a = 0
    b = len(key_list) - 1

    if key_list[a] == key:
        return a

    if key_list[b] == key:
        return b

    while True:

        x = int((a + b) / 2)

        if a == x:
            if first_lower:
                return key_list[x]
            else:
                return None

        if key_list[x] == key:
            return x
        elif key_list[x] > key:
            b = x
        else:
            a = x

