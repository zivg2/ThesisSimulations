from projective_sets.pgl import PGL


def get_q_groups_from_file(filename):
    result = {}
    with open(filename) as file:
        for group_data in file:
            if group_data == '\n':
                continue
            first_comma = group_data.index(',')
            q = int(group_data[:first_comma])
            pgl = PGL(2, q)
            field = pgl.get_field()
            if q not in result:
                result[q] = []
            group_data = group_data[first_comma+4:-3]
            elements = []
            element_strings = group_data.split('], [')
            for element_string in element_strings:
                rows = element_string.split(';')
                element_data = [row.split(',') for row in rows]
                element_data = [[field.create_element(int(x)) for x in row] for row in element_data]
                element = pgl.create(element_data)
                elements.append(element)
            result[q].append(set(elements))
    return result
