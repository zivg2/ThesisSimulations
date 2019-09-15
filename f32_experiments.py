from fields.f32 import F32

f32 = F32()

elements = f32.get_all_elements()


def get_bad_y(x):
    result = []
    one = f32.one()
    for i in [1, 2, 4, 8, 16]:
        result.append(x ** i)
        result.append(x.inverse() ** i)
        result.append(one-x ** i)
        result.append((x ** i - one)/(x ** i))
        result.append((one-x ** i).inverse())
        result.append((x ** i)/(x ** i - one))

    result.append(one)
    result.append(f32.zero())
    return set(result)


for x in elements:
    if x == f32.zero() or x == f32.one():
        continue
    bad_y = get_bad_y(x)
    print(x, len(bad_y))
