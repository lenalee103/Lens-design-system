
from CalculateAberration import cfunc
from CalculateBending import cBending
import matplotlib.pyplot as plt
from CalculateDistances import cDistances
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


wavelength = 1.064
h = 2
h_in = 2.
h_out = 1.0 / 2.8 * 2.0
lens1_r1 = 29.85
lens1_r2 = -29.85
lens1_n = 1.50663348492911
lens1_t = 7.74

lens2_r1 = -7.
lens2_r2 = 1e+12
lens2_n = 1.75389272961219
lens2_t = 2.

lens3_r1 = 38.6
lens3_r2 = 1e+12
lens3_n = 1.50663348492911
lens3_t = 4.1


def A(x, y, z):
    LensBend1 = cBending(x, lens1_n, lens1_r1, lens1_r2)
    r11 = LensBend1[0]
    r12 = LensBend1[1]
    LensBend2 = cBending(y, lens2_n, lens2_r1, lens2_r2)
    r21 = LensBend2[0]
    r22 = LensBend2[1]
    LensBend3 = cBending(z, lens3_n, lens3_r1, lens3_r2)
    r31 = LensBend3[0]
    r32 = LensBend3[1]
    distance = cDistances(h_in, h_out, r11, r12, lens1_n, lens1_t, r21, r22, lens2_n, lens2_t, r31, r32, lens3_n,
                          lens3_t)
    aberration = cfunc(wavelength, h, distance[0], distance[1], r11, r12, lens1_n, lens1_t, r21, r22, lens2_n, lens2_t,
                       r31, r32, lens3_n, lens3_t)

    return aberration

def f(x, y, z, lout=None):
    it = np.nditer([x, y, z, lout], [], [['readonly'], ['readonly'], ['readonly'],['writeonly', 'allocate']])
    for (a, b, c, aberration) in it:
        aberration = A(a, b, c)

    return it.operands[2]


x = np.random.standard_normal(1000)
y = np.random.standard_normal(1000)
z = np.random.standard_normal(1000)

c = abs(f(x, y, z))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_zlabel('CF3')
ax.set_ylabel('CF2')
ax.set_xlabel('Cf1')
im = ax.scatter(x, y, z, c=c, cmap='coolwarm')
# ax.view_init(60, 35)
plt.colorbar(im)
plt.show()







#plt.plot(cf, r1, 'rx')
#plt.plot(cf, r2, 'go')
#plt.xlabel('CoddingFactor')
#plt.ylabel('Radius Change')
#plt.show()

#plt.plot(cf, d1, 'ro')
#plt.plot(cf, d2, 'gx')
#plt.xlabel('CoddingFactor')
#plt.ylabel('Distance Change')
#plt.show()

#plt.plot(cf, aberration, 'yx')
#plt.xlabel('CoddingFactor')
#plt.ylabel('Aberration Change')
#plt.show()


