from itertools import product, permutations

from partitions import Partition


def get_circle_results(n, tables):
    results = list()
    results.append((Partition([n]), Partition([0]), [Partition([n])]))
    results.append((Partition([1]*n), Partition([0]), [Partition([1]*n)]))
    table = tables[n]
    for k1, k2 in [(n-x, x) for x in range(1, n // 2 + 1)]:
        table1 = tables[k1]
        table2 = tables[k2]
        for mu1, mu2 in product(table1.partitions, table2.partitions):
            result = []
            for nu in table.partitions:
                coefficients = []
                for a1, a2 in product(table1.partitions, table2.partitions):
                    partition_union = a1.union(a2)
                    value1 = table1.inverse_kostka(a1, mu1)
                    value2 = table2.inverse_kostka(a2, mu2)
                    value3 = table.kostka(nu, partition_union)
                    value = value1 * value2 * value3
                    coefficients.append(value)
                coefficients_sum = sum(coefficients)
                result.append(coefficients_sum)
            summands = []
            for i in range(len(table.partitions)):
                for _ in range(result[i]):
                    summands.append(table.partitions[i].conjugate())
            results.append((mu1.conjugate(), mu2.conjugate(), summands))
    return results


def difference(lists):
    result = {}
    list_union = []
    for l in lists:
        list_union.extend(l)
    for coefficients in product([1, -1], repeat=len(lists)):
        result[coefficients] = []
        for x in set(list_union):
            coefficient = sum([lists[i].count(x) * coefficients[i] for i in range(len(lists))])
            if coefficient != 0:
                result[coefficients].append((coefficient, x))
    return result


def get_difference_data(results, max_decomposition_length):
    data = {}
    exhausted_answers = []
    for decomposition_parts in range(1, max_decomposition_length + 1):
        for lines in permutations(results, r=decomposition_parts):
            a = difference([x[2] for x in lines])
            for coefficients in a:
                if len(a[coefficients]) == 1 and a[coefficients][0][0] == 1:
                    character_partition = a[coefficients][0][1]
                    answer_data = set((coefficients[i], lines[i][:2]) for i in range(len(lines)) if coefficients[i] != 0)
                    if answer_data in exhausted_answers:
                        continue
                    exhausted_answers.append(
                        answer_data
                    )
                    if character_partition not in data:
                        data[character_partition] = []
                    data[character_partition].append(answer_data)
    return data


def print_difference_data(difference_data):
    for character_partition in difference_data:
        for decomposition in difference_data[character_partition]:
            sorted_decomposition = sorted(decomposition, key=lambda x: x[1][1].n())
            answer = "%s = " % (character_partition,)
            s = 0
            for coefficient, x in sorted_decomposition:
                s += abs(coefficient)
                if coefficient == 1:
                    answer += "+%s" % str(x)
                elif coefficient == -1:
                    answer += "-%s" % str(x)
            print(answer)


def print_difference_data_length_bound(difference_data):
    for character_partition in difference_data:
        for decomposition in difference_data[character_partition]:
            sorted_decomposition = sorted(decomposition, key=lambda x: x[1][1].n())
            answer = "%s" % (character_partition,)
            answer += " = "
            if len(sorted_decomposition) > min(len(character_partition), len(character_partition.conjugate())):
                continue
            s = 0
            for coefficient, x in sorted_decomposition:
                s += abs(coefficient)
                if coefficient == 1:
                    answer += "+%s" % str(x)
                elif coefficient == -1:
                    answer += "-%s" % str(x)
            print(answer)
