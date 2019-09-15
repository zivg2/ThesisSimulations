from representations.characters import Character
from symmetric_group.sn import SNElement


class SignCharacter(Character):
    def apply(self, x: SNElement) -> float:
        return x.sign()

    def __str__(self):
        return "sgn"
