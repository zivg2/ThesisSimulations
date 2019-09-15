from representations.characters import Character
from symmetric_group.sn import SNElement
from typing import Dict
from partitions import Partition


class SNTableCharacter(Character):
    def __init__(self, character_table: Dict[Partition, float], name: str):
        self._conjugation_class_to_value = character_table
        self.name = name

    def apply(self, x: SNElement) -> float:
        conjugation_class = x.conjugation_class()
        return self._conjugation_class_to_value[conjugation_class]

    def __str__(self):
        return self.name

