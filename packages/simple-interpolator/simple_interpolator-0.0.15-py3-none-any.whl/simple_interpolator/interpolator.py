import matplotlib.pyplot as plt
import numpy as np
import functools
import math
from simple_interpolator.stylizer import f_as_text

class Interpolator:
    def __init__(self, data):
        self.data = data
        self.__power_touples = self.__generate_power_touples()
        self.__b = self.__generate_b()
        self.f = self.__generate_f()

    def __generate_power_touples(self):
        rank = math.ceil(len(self.data)**0.5)-1
        return [[i, j] for j in range(rank+1) for i in range(rank+1)]

    def __generate_b(self):
        def power_values(x, y):
            return [x**p_t[0]*y**p_t[1] for p_t in self.__power_touples]

        A = [power_values(touple[0], touple[1]) for touple in self.data]
        At = np.transpose(A)
        f = list(map(lambda touple : touple[2], self.data))

        return np.linalg.solve(np.matmul(At, A), np.matmul(At, f))

    def __generate_f(self):
        def f(x, y):
            return sum([self.__b[i]*x**powers[0]*y**powers[1] for i, powers in enumerate(self.__power_touples)])
        return f

    def print_f(self, accuracy=-1):
        print(f_as_text(self.__b, self.__power_touples,accuracy))

    def show(self, knots_per_unit=10):
        kpu = knots_per_unit
        def bound(f, axis_id):
            return functools.reduce(lambda acc, touple : f(touple[axis_id], acc), self.data, self.data[0][axis_id])

        X = np.outer(np.linspace(bound(min, 0), bound(max, 0), kpu), np.ones(kpu))
        Y = np.outer(np.linspace(bound(min, 1), bound(max, 1), kpu), np.ones(kpu)).T
        Z = self.f(X, Y)
        ax = plt.axes(projection ='3d')
        ax.plot_surface(X, Y, Z)
        [ax.scatter(touple[0], touple[1], touple[2]) for touple in self.data]
        plt.show()