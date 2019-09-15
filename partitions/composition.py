from utilities.general_utilities import class_property_memorize


class Composition:
    @staticmethod
    def sub_compositions(composition, s):
        if len(composition) == 0:
            return []
        elif len(composition) == 1:
            return [Composition([s])] if composition[0] >= s else []
        result = []
        for i in range(0, min(composition[-1], s) + 1):
            previous_sub_compositions = Composition.sub_compositions(composition[:-1], s - i)
            added_sub_compositions = [x.extended_by_element(i) for x in previous_sub_compositions]
            result.extend(added_sub_compositions)
        return result

    def __init__(self, sequence):
        self.sequence = sequence

    @class_property_memorize
    def n(self):
        return sum(self.sequence)

    @class_property_memorize
    def trimmed_sequence(self):
        return tuple([x for x in self.sequence if x != 0])

    @class_property_memorize
    def padded_sequence(self, k):
        coefficients = [x for x in self.sequence]
        coefficients += [0] * (k - len(self))
        return tuple(coefficients)

    def union(self, other):
        united_list = list(self.sequence) + list(other.sequence)
        return Composition(united_list)

    def extended_by_element(self, element):
        united_list = list(self.sequence)
        united_list.append(element)
        return Composition(united_list)

    def __add__(self, other):
        result_list = []
        for i in range(max(len(self), len(other))):
            result_list.append(self[i] + other[i])
        return Composition(result_list)

    def __len__(self):
        return len(self.sequence)

    def __getitem__(self, item):
        if item < len(self):
            return self.sequence[item]
        else:
            return 0

    def __str__(self):
        return str(self.sequence)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(tuple(self.sequence))

    def __eq__(self, other):
        for i in range(len(self)):
            if self.sequence[i] != other.sequence[i]:
                return False
        return True
