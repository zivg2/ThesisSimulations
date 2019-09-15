from symmetric_group import SN
from itertools import permutations


s4 = SN(4)


def c4a(a, b, c, d):
    elements = list()
    elements.append({a: a, b: b, c: c, d: d})
    elements.append({a: b, b: a, c: d, d: c})
    elements.append({a: d, b: c, c: a, d: b})
    elements.append({a: c, b: d, c: b, d: a})
    return elements


def k4(a, b, c, d):
    elements = list()
    elements.append({a: a, b: b, c: c, d: d})
    elements.append({a: b, b: a, c: d, d: c})
    elements.append({a: c, b: d, c: a, d: b})
    elements.append({a: d, b: c, c: b, d: a})
    return elements


def transitive_minimal_subgroups(elements):
    a, b, c, d = elements
    subgroups = list()
    subgroups.append(c4a(a, b, c, d))
    subgroups.append(c4a(b, c, a, d))
    subgroups.append(c4a(c, a, b, d))
    subgroups.append(k4(a, b, c, d))
    return subgroups


for order in permutations([4, 5, 6]):
    set1 = [1, 2, 3, order[0]]
    for subgroup in transitive_minimal_subgroups(set1):
        good_images = set()
        for element in subgroup:
            image1 = tuple([element[x] for x in set1])
            if order[0] in image1[:3]:
                good_images.add(image1[:3])
        for image1 in good_images:
            set2 = list(image1) + [order[1]]
            for subgroup2 in transitive_minimal_subgroups(set2):
                good_images2 = set()
                for element in subgroup2:
                    image2 = tuple([element[x] for x in set2])
                    if order[0] in image2[:3] and order[1] in image2[:3]:
                        good_images2.add(image2[:3])
                for image2 in good_images2:
                    set3 = list(image2) + [order[2]]
                    for subgroup3 in transitive_minimal_subgroups(set3):
                        good_images3 = set()
                        for element in subgroup3:
                            image3 = tuple([element[x] for x in set3])
                            if order[0] == image3[0] and order[1] == image3[1] and order[2] == image3[2]:
                                good_images3.add(image3[:3])
                        print(good_images3)