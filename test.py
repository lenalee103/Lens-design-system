
from CalculateAberration import cfunc
from CalculateBending import cBending
import matplotlib.pyplot as plt
from CalculateDistances import cDistances
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

r11 = []
r12 = []
cf1 = []
r21 = []
r22 = []
cf2 = []
r31 = []
r32 = []
cf3 = []

d1 = []
d2 = []
aberration = [[0]*100 for _ in range(100)]
coddingtonFactor1 = -1
coddingtonFactor2 = -1
coddingtonFactor3 = -1
cf1.append(-1)
cf2.append(-1)
cf3.append(-1)


r11.append(29.85)
r12.append(-29.85)
r21.append(-7)
r22.append(1e+12)
r31.append(38.6)
r32.append(1e+12)

d1.append(0.05)
d2.append(0.05)
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

aberration0 = cfunc(wavelength, h, d1[0], d2[0], lens1_r1, lens1_r2, lens1_n, lens1_t, lens2_r1, lens2_r2, lens2_n,
                    lens2_t, lens3_r1, lens3_r2, lens3_n, lens3_t)
aberration[0][0] = aberration0

for i in range(99):
    coddingtonFactor1 += 0.05
    LensBend1 = cBending(coddingtonFactor1, lens1_n, r11[i], r12[i])
    cf1.append(coddingtonFactor1)
    r11.append(LensBend1[0])
    r12.append(LensBend1[1])

    coddingtonFactor2 += 0.05
    LensBend2 = cBending(coddingtonFactor2, lens2_n, r21[i], r22[i])
    cf2.append(coddingtonFactor2)
    r21.append(LensBend2[0])
    r22.append(LensBend2[1])

    coddingtonFactor3 += 0.05
    LensBend3 = cBending(coddingtonFactor3, lens3_n, r31[i], r32[i])
    cf3.append(coddingtonFactor3)
    r31.append(LensBend3[0])
    r32.append(LensBend3[1])

for i in range(99):
    for j in range(99):
        distance = cDistances(h_in, h_out, r11[i+1], r12[i+1], lens1_n, lens1_t, r21[j+1], r22[j+1], lens2_n, lens2_t,
                              lens3_r1, lens3_r2, lens3_n, lens3_t)
        aberration[i+1][j+1] = cfunc(wavelength, h, distance[0], distance[1], r11[i+1], r12[i+1], lens1_n, lens1_t,
                                     r21[j + 1], r22[j + 1], lens2_n, lens2_t, r31[j+1], r32[j+1], lens3_n, lens3_t)


def f(x,y):
    return np.array(aberration)[x][y]


x = np.arange(0, 100, 1)
y = np.arange(0, 100, 1)
# z = np.array(aberration)[x][y]
z = np.abs(f(x, y))
x = np.asarray(cf1)
y = np.asarray(cf2)
xs, ys = np.meshgrid(x, y)

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(xs, ys, z, cmap='coolwarm')



#ax = plt.axes(projection='3d')
#ax.scatter3D(x, y, z, c=z, cmap='Greens')

#ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.set_xlabel('cf1')
ax.set_ylabel('cf2')
ax.set_zlabel('Aberration')
ax.view_init(60, 35)
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


