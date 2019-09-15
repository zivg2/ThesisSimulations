from circle_sum_decompositions import *
from partitions.kostka_table import get_tables

n = 6

tables = get_tables(n)

results = get_circle_results(n, tables)
for line in results:
    print(line)


print()


data = get_difference_data(results, round(n/2))
new_data = {}

for partition in data:
    new_data[partition] = []
    for difference in data[partition]:
        if len(difference) > len(partition):
            continue
        sorted_difference = sorted(difference, key=lambda x: x[1][1].n())
        sorted_difference_with_values = []
        bad_pair = False
        for pair in sorted_difference:
            value = pair[1][0].conjugate().n_lambda() \
                    + pair[1][1].conjugate().n_lambda() \
                    - partition.conjugate().n_lambda()
            if value > 0:
                bad_pair = True
            sorted_difference_with_values.append((pair[0], pair[1], value))
        if not bad_pair:
            new_data[partition].append(sorted_difference_with_values)


print()
print_difference_data_length_bound(new_data)
