from representations.characters import Character
from symmetric_group.sn import SNElement


class StandardCharacter(Character):
    def apply(self, x: SNElement) -> float:
        orbits = x.get_orbits()
        fixed_points = len([orbit for orbit in orbits if len(orbit) == 1])
        return fixed_points - 1

    def __str__(self):
        return "std"
