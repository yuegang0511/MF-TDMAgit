def get_list(slot, frequency):
    n = []
    for i in range(slot):
        fre = []
        for j in range(frequency):
            fre.append(j)
        n.append(fre)
    return n

a = get_list()
a[0]
print(get_list(3, 4))