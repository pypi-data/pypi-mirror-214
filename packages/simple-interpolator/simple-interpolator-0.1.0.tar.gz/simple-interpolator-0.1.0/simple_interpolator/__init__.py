# from simple_interpolator.interpolator import Interpolator
from interpolator import Interpolator

i = Interpolator([(2,-5,2),(6,-3,4),(3,-6,4),(-4,3,5),(5,-4,8),(3,7,-5)])

print("Provided coordinates:\n\n\t", i.data, "\n")

print("An interpolant:\n\n",end='\t')
i.print_f(1)

i.graph()
i.colormap()

i.show()