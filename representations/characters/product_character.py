from .character import Character


class ProductCharacter(Character):
    def __init__(self, character1: Character, character2: Character):
        self._character1 = character1
        self._character2 = character2

    def apply(self, x) -> float:
        return self._character1.apply(x)*self._character2.apply(x)

    def __str__(self):
        return '%s*%s' % (str(self._character1), str(self._character2))
