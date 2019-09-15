from partitions import Partition


class SNElement:
    def __init__(self, permutation, group):
        self._permutation = tuple(permutation)
        self._group = group

    def __mul__(self, other):
        permutation = [self._permutation[other._permutation[x]] for x in range(self._group.n)]
        return self._group.create_element(permutation)

    def inverse(self):
        permutation = [-1] * self._group.n
        for i in range(self._group.n):
            permutation[i] = self._permutation.index(i)
        return self._group.create_element(permutation)

    def __getitem__(self, item):
        return self._permutation[item]

    def sign(self):
        parity = 1
        lst = [x for x in self._permutation]
        for i in range(len(lst)-1):
            if lst[i] != i:
                parity *= -1
                mn = min(range(i, len(lst)), key=lst.__getitem__)
                lst[i], lst[mn] = lst[mn], lst[i]
        return parity

    def __str__(self):
        orbits = self.get_orbits()
        result = "".join(str(orbit) for orbit in orbits if len(orbit) > 1)
        if result == "":
            result = "()"
        return result

    def get_orbits(self):
        elements = list(range(self._group.n))
        orbits = []
        while len(elements) > 0:
            orbit_representative = elements[0]
            orbit = []
            x = orbit_representative
            while x not in orbit:
                orbit.append(x)
                elements.remove(x)
                x = self[x]
            orbits.append(tuple(orbit))
        return orbits

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self._permutation == other._permutation

    def __hash__(self):
        return hash(self._permutation)

    def conjugation_class(self):
        orbits = self.get_orbits()
        orbits_lengths = sorted([len(x) for x in orbits])
        return Partition(orbits_lengths)


