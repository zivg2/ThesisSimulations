from . import Representation
from .characters.trivial_character import Character, TrivialCharacter
import numpy as np


class TrivialRepresentation(Representation):
    def apply(self, x) -> np.ndarray:
        return np.ones((1, 1))

    def dim(self) -> int:
        return 1

    def get_character(self) -> Character:
        return TrivialCharacter()

    def __str__(self):
        return 'triv'
