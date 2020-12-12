
def bisection(key, key_list):

    a = 0
    b = len(key_list) - 1

    if key_list[a] == key:
        return True, a

    if key_list[b] == key:
        return True, b

    if key_list[b] < key:
        return False, b

    while True:

        x = int((a + b) / 2)

        if a == x:
            return False, x

        if key_list[x] == key:
            return True, x
        elif key_list[x] > key:
            b = x
        else:
            a = x

