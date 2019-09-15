from symmetric_group import SN


def get_a4_generators():
    sn = SN(4)
    an_elements = [x for x in sn.get_all_elements() if x.sign() == 1]
    for x in an_elements:
        for y in an_elements:
            group = {sn.identity(),
                     x, y,
                     x * x, y * x, x * y, y * y, y * x,
                     x * x * y, y * x * y, x * y * y, y * y * y,
                     x * x * x, y * x * x, x * y * x, y * y * x
                     }
            if len(group) > 6:
                return x, y
    return None
