from .prime_field_element import PrimeFieldElement
from .field_with_product_table import FieldWithProductTable
from utilities.general_utilities import class_property_memorize, measure
from typing import List
from itertools import product


class PrimeField(FieldWithProductTable):
    def __init__(self, p: int):
        self._p = p
        self._creation_table = [PrimeFieldElement(n, self._p, self) for n in range(self._p)]
        self._product_table = {(a, b): self.create_element(a * b) for a, b in product(range(p), repeat=2)}

    @measure
    def create_element(self, n: int) -> PrimeFieldElement:
        return self._creation_table[n % self._p]

    @class_property_memorize
    def zero(self) -> PrimeFieldElement:
        return self.create_element(0)

    @class_property_memorize
    def one(self) -> PrimeFieldElement:
        return self.create_element(1)

    @class_property_memorize
    def get_all_elements(self) -> List[PrimeFieldElement]:
        return [self.create_element(n) for n in range(self._p)]

    def size(self) -> int:
        return self._p

    def get_product(self, a: PrimeFieldElement, b: PrimeFieldElement) -> PrimeFieldElement:
        return self._product_table[(a.n, b.n)]

    def get_base_element(self, element: PrimeFieldElement) -> PrimeFieldElement:
        return element

    def trace(self, element: PrimeFieldElement) -> PrimeFieldElement:
        return element

    def norm(self, element: PrimeFieldElement) -> PrimeFieldElement:
        return element







