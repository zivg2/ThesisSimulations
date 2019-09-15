from numpy.polynomial import Polynomial, polynomial
from numpy import ndarray


class MyPolynomial:
    @classmethod
    def get_x(cls):
        return cls(polynomial.polyx)

    def __init__(self, *args, **kwargs):
        if isinstance(args[0], Polynomial):
            self.polynomial = args[0]
        elif isinstance(args[0], ndarray):
            self.polynomial = Polynomial(args[0])
        else:
            self.polynomial = Polynomial(*args, **kwargs)

    def __neg__(self):
        return MyPolynomial(-self.polynomial)

    def __add__(self, other):
        if isinstance(other, MyPolynomial):
            return MyPolynomial(polynomial.polyadd(self.polynomial, other.polynomial)[0])
        else:
            return MyPolynomial(self.polynomial + other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, MyPolynomial):
            return MyPolynomial(polynomial.polysub(self.polynomial, other.polynomial)[0])
        else:
            return MyPolynomial(self.polynomial - other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, MyPolynomial):
            return MyPolynomial(polynomial.polymul(self.polynomial, other.polynomial)[0])
        else:
            return MyPolynomial(self.polynomial * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return MyPolynomial(self.polynomial / other)

    def __str__(self):
        return self.get_string()

    def get_string(self):
        result = ''
        for i in range(self.polynomial.degree(), -1, -1):
            coefficient = self.polynomial.coef[i]
            degree = i
            s = "x**" + str(degree)
            if degree == 0 and coefficient != 0:
                result += "+%.2f" % coefficient
            elif coefficient == 1:
                result += "+%s" % s
            elif coefficient == -1:
                result += "-%s" % s
            elif coefficient > 0:
                result += "+%.2f%s" % (coefficient, s)
            elif coefficient < 0:
                result += "-%.2f%s" % (-coefficient, s)
        if result == '':
            result = '0'
        return result
