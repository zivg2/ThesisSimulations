import re
from scipy.misc import comb
from math import gcd


DECOMPOSITION_DATA_START = '===='
Q_VALUE_PREFIX = 'q='
DATA_PREFIX = 'wedge(std, '

TRIV = 'triv'
SGN = 'sgn'
STD = 'std'
STD_SGN = '^std'
RHO = 'ρ'
PI = 'π'

representations_dimensions = {
    TRIV: (lambda _: 1),
    SGN: (lambda _: 1),
    STD: (lambda q: q),
    STD_SGN: (lambda q: q),
    RHO: (lambda q: q + 1),
    PI: (lambda q: q-1)
}

numbers_re = re.compile('\d*')
letters_re = re.compile('\D*')


def analyze_decomposition(decomposition_string: str):
    if decomposition_string == '\n':
        return []
    result = []
    elements = decomposition_string.split('+')
    for element in elements:
        numbers_matching = numbers_re.findall(element)
        name_matching = letters_re.findall(element)
        quantity_present = name_matching[0] == ''

        name = [x for x in name_matching if x != ''][0]
        if name[-1] == '\n':
            name = name[:-1]

        index_index = 2 if quantity_present else 1

        if name not in [RHO, PI, STD, SGN, STD_SGN, TRIV]:
            print(name)

        quantity = int(numbers_matching[0]) if quantity_present else 1
        index = int(numbers_matching[index_index]) if numbers_matching[index_index] != '' else -1
        result.append((quantity, name, index))

    return result


with open('character_decompositions.txt', encoding='utf-8') as decompositions:
    global q
    data = {}
    line = ''
    while not line.startswith(DECOMPOSITION_DATA_START):
        line = decompositions.readline()
    for line in decompositions:
        if line.startswith(Q_VALUE_PREFIX):
            q = int(line[len(Q_VALUE_PREFIX):])
        if line.startswith(DATA_PREFIX):
            closing_location = line.find(')')
            i = int(line[len(DATA_PREFIX): closing_location])
            decomposition_string = line[closing_location+2:]
            decomposition = analyze_decomposition(decomposition_string)
            data[(q, i)] = decomposition

    simplified_data = {}
    for pair in data:
        pair_data = data[pair]
        simplified_data[pair] = {}
        for x in pair_data:
            quantity, name, _ = x
            if name not in simplified_data[pair]:
                simplified_data[pair][name] = 0
            simplified_data[pair][name] += quantity

    qs_dimensions = {}
    qs = set([x[0] for x in simplified_data])
    for q in qs:
        q_simplified_data = {pair[1]: simplified_data[pair] for pair in simplified_data if pair[0] == q}
        q_dimensions = {i: sum(
            [representations_dimensions[name](q)*q_simplified_data[i][name] for name in q_simplified_data[i]]
                               ) for i in q_simplified_data}

        q_dimensions2 = {i: (q_dimensions[i], comb(q, i)) for i in q_dimensions}
        qs_dimensions[q] = q_dimensions2

    rho_data = {}
    for pair in data:
        pair_data = data[pair]
        rho_data[pair] = {}
        for x in pair_data:
            quantity, name, index = x
            if name == RHO:
                index_gcd = gcd(index, (pair[0]-1))
                if index_gcd in rho_data[pair] and rho_data[pair][index_gcd] != quantity:
                    print(pair, x)
                else:
                    rho_data[pair][index_gcd] = quantity

    pi_data = {}
    for pair in data:
        pair_data = data[pair]
        pi_data[pair] = {}
        for x in pair_data:
            quantity, name, index = x
            if name == PI:
                index_gcd = gcd(index, (pair[0]+1))
                if index_gcd in pi_data[pair] and pi_data[pair][index_gcd] != quantity:
                    print(pair, x)
                else:
                    pi_data[pair][index_gcd] = quantity

    i = 3
    simplified_data_for_i = {x[0]: simplified_data[x] for x in simplified_data if x[1] == i}
    print(simplified_data_for_i)
    print(simplified_data)