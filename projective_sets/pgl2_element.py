from fields import Field, FieldElement
from projective_sets.pgl_element import PGLElement
from utilities.general_utilities import class_property_memorize


class PGL2Element(PGLElement):
    def __init__(self,
                 a: FieldElement, b: FieldElement,
                 c: FieldElement, d: FieldElement,
                 pgl2):
        super().__init__(((a, b), (c, d)), pgl2)
        self.a = self.coefficients[0][0]
        self.b = self.coefficients[0][1]
        self.c = self.coefficients[1][0]
        self.d = self.coefficients[1][1]

    @class_property_memorize
    def det(self) -> FieldElement:
        return self.a * self.d - self.b * self.c

    @class_property_memorize
    def inverse(self):
        return PGL2Element(self.d, -self.b, -self.c, self.a, self.pgl)

