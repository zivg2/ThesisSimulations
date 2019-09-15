
total_possible_orders = {'S4': 48*2,
                         'A4': 24*2,
                         'A5': 120*2/5}


def possible_orders(q):
    result_keys = []
    if q % 8 == 1 or q % 8 == 7:
        result_keys.append('S4')
    if q % 8 == 3 or q % 8 == 5:
        result_keys.append('A4')
    if q % 10 == 1 or q % 10 == 9:
        result_keys.append('A5')
    return {x: total_possible_orders[x] for x in result_keys}


for q in range(2, max(total_possible_orders.values())):
    x = (q + 1)

    orders = possible_orders(q)
    for order_key in orders:
        order = orders[order_key]
        if order % x == 0:
            print(q, x, order_key)