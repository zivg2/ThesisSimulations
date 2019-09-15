from symmetric_group import SN

s4 = SN(4)


def get_subgroup(element1, element2):
    subgroup = set()
    current = element1
    for i in range(4):
        subgroup.add(current)
        current *= element1

    extension = []
    for x in subgroup:
        current = x
        for i in range(4):
            current *= element2
            extension.append(current)

    for x in extension:
        subgroup.add(x)

    extension = []
    for x in subgroup:
        current = x
        for i in range(4):
            current *= element1
            extension.append(current)
    for x in extension:
        subgroup.add(x)

    extension = []
    for x in subgroup:
        current = x
        for i in range(4):
            current *= element2
            extension.append(current)
    for x in extension:
        subgroup.add(x)
    extension = []
    for x in subgroup:
        current = x
        for i in range(4):
            current *= element1
            extension.append(current)
    for x in extension:
        subgroup.add(x)
    extension = []
    for x in subgroup:
        current = x
        for i in range(4):
            current *= element2
            extension.append(current)
    for x in extension:
        subgroup.add(x)

    return subgroup


for element in s4.get_all_conjugation_classes():
    if element == s4.identity():
        continue
    for element2 in s4.get_all_elements():
        if element2 == s4.identity():
            continue
        subgroup = get_subgroup(element, element2)
        s = len(subgroup)
        if s not in [24, 12]:
            print(len(subgroup), subgroup)
