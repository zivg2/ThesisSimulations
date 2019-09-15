from .character import Character


class TrivialCharacter(Character):
    def apply(self, x) -> float:
        return 1

    def __str__(self):
        return 'χ_triv'
