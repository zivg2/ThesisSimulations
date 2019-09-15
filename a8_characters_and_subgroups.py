from symmetric_group import SN
from elements_generator.conditional_elements_generator import ConditionalElementsGenerator

S8 = SN(8)
A8 = ConditionalElementsGenerator(S8, lambda x: x.sign() == 1)

for x in A8.get_all_elements():
    print(x)