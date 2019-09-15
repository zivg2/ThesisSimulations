from itertools import combinations, permutations, chain, product
import time
import numpy as np
from matplotlib.pyplot import subplots


_measure_dictionary = {}


def memorize(f):
    memorization_dictionary = {}

    def helper(*args):
        if args not in memorization_dictionary:
            memorization_dictionary[args] = f(*args)
        return memorization_dictionary[args]
    helper.__module__ = f.__module__
    helper.__name__ = f.__name__
    return helper


def class_property_memorize(f):
    name = f.__name__ + "_memorization"

    def helper(*args):
        self_arg = args[0]
        if name not in self_arg.__dict__:
            self_arg.__dict__[name] = f(*args)
        return self_arg.__dict__[name]
    helper.__module__ = f.__module__
    helper.__name__ = f.__name__
    return helper


def measure(f):
    name = f.__module__ + "." + f.__name__
    if name not in _measure_dictionary:
        _measure_dictionary[name] = [0, 0]

    def helper(*args, **kw):
        start_time = time.time()
        result = f(*args, **kw)
        duration = time.time() - start_time
        _measure_dictionary[name][0] += duration
        _measure_dictionary[name][1] += 1
        return result

    return helper


def get_measure_mapping():
    mapping = sorted(_measure_dictionary.items(), key=lambda kv: kv[1][0], reverse=True)
    mapping = [(x[0], x[1][0], x[1][1], x[1][0]/x[1][1]) for x in mapping if x[1][0] > 0]
    return mapping


def power_set(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def round_up_to(number, denominator=100000):
    number *= denominator
    number = round(number)
    number /= denominator
    return number


def plot_complex_list(complex_list, color='b'):
    fig, ax = subplots()
    ax.scatter(np.real(complex_list), np.imag(complex_list), c=color)
    fig.show()
    fig.waitforbuttonpress()


def plot_complex_lists(complex_lists):
    fig, ax = subplots()
    colors = ['r', 'g', 'b', 'y']
    i = 0
    for complex_list in complex_lists:
        ax.scatter(np.real(complex_list), np.imag(complex_list), c=colors[i])
        i += 1
    fig.show()
    fig.waitforbuttonpress()


def get_rho(d):
    return 2 * np.sqrt(d - 1)


def subsets(s):
    sets = []
    for i in range(1 << len(s)):
        subset = [s[bit] for bit in range(len(s)) if is_bit_set(i, bit)]
        sets.append(subset)
    return sets


def is_bit_set(num, bit):
    return num & (1 << bit) > 0


def number_to_coefficient_string(number, parameter):
    parameter_string = str(parameter)
    if number == 1:
        return "+%s" % parameter_string
    elif number == -1:
        return "-%s" % parameter_string
    elif number > 0:
        return "+%d%s" % (number, parameter_string)
    elif number < 0:
        return "-%d%s" % (-number, parameter_string)
    else:
        return ""
