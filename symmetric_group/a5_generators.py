from symmetric_group import SN


def get_a5_generating_words():
    sn = SN(5)
    v5 = sn.create_element([1, 2, 3, 4, 0])
    v2 = sn.create_element([1, 0, 3, 2, 4])
    group = {sn.identity(): ''}
    while len(group) < 60:
        group_additions = {}
        for x in group:
            if x*v5 not in group and x*v5 not in group_additions:
                group_additions[x*v5] = group[x] + '*v5'
            if x*v2 not in group and x*v2 not in group_additions:
                group_additions[x*v2] = group[x] + '*v2'
        for addition in group_additions:
            text = group_additions[addition]
            group[addition] = text if text[0] != '*' else text[1:]

    return list(group.values())
