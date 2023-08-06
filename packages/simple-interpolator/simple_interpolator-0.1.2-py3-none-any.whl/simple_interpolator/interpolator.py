import matplotlib.pyplot as plt
import numpy as np
import functools
import math
from simple_interpolator.stylizer import f_as_text

class Interpolator:
    data = []
    __power_touples = []
    __b = []
    f = None
    rank = -1

    def __init__(self, data, rank=-1):
        self.data = data
        self.rank = rank
        self.__generate_f()

    def __generate_power_touples(self):
        rank = math.ceil(len(self.data)**0.5)-1 if self.rank == -1 else self.rank
        return [[i, j] for j in range(rank+1) for i in range(rank+1)]

    def __generate_b(self):
        def power_values(x, y):
            return [x**p_t[0]*y**p_t[1] for p_t in self.__power_touples]

        A = [power_values(touple[0], touple[1]) for touple in self.data]
        At = np.transpose(A)
        f = list(map(lambda touple : touple[2], self.data))

        return np.linalg.solve(np.matmul(At, A), np.matmul(At, f))

    def __generate_f(self):
        print("ehere")
        self.__power_touples = self.__generate_power_touples()
        self.__b = self.__generate_b()
        self.f = lambda x, y : sum([self.__b[i]*x**powers[0]*y**powers[1] for i, powers in enumerate(self.__power_touples)])

    def print_f(self, accuracy=-1):
        print(f_as_text(self.__b, self.__power_touples,accuracy))

    def add_coordinates(self, coordinates):
        self.data += coordinates
        self.__generate_f()

    def add_coordinate(self, coordinate):
        self.data += [coordinate]
        self.__generate_f()

    def set_rank(self, rank):
        self.rank = rank
        self.__generate_f()
    
    def auto_rank(self):
        self.rank = -1
        self.__generate_f()

    def __getXYZ(self, knots_per_unit):
        bound = lambda f, axis_id : functools.reduce(lambda acc, touple : f(touple[axis_id], acc), self.data, self.data[0][axis_id])

        X, Y = np.meshgrid(
                np.linspace(bound(min, 0), bound(max, 0), knots_per_unit), 
                np.linspace(bound(min, 1), bound(max, 1), knots_per_unit))
        
        Z = self.f(X, Y)
        return X, Y, Z

    def graph(self, knots_per_unit=10, alpha=1, show_provided=False):
        X,Y,Z = self.__getXYZ(knots_per_unit)

        ax = plt.subplot(projection ='3d')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.plot_surface(X, Y, Z, alpha=alpha)
        if show_provided:
            [ax.scatter(touple[0], touple[1], touple[2], c='g') for touple in self.data]

    def colormap(self, knots_per_unit=1000):
        X,Y,Z = self.__getXYZ(knots_per_unit)

        fig, ax = plt.subplots()
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        pc = ax.pcolormesh(X, Y, Z, cmap='RdBu_r')
        fig.colorbar(pc, ax=ax)

    def show(self):
        plt.show()