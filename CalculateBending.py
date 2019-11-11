from ctypes import *
import os
import matplotlib.pyplot as plt

path = 'C:/Users/rf613258\Desktop/brain_and_b1\calculateBending'    	# path to .dll file
os.chdir(path)

cBending = cdll.LoadLibrary('./calculateBending.dll').bendLens
cBending.argtypes = [c_double, c_double, c_double, c_double] 				# arguments types
cBending.restype = POINTER(c_double)    # return type, or None if void

#cF3 = 0.5
#lens3_n = 1.50663348492911
#lens3_t = 4.1
#lens3_r1 = 38.6
#lens3_r2 = 1e+12
#lens3_r1_ = cBending(cF3, lens3_n, lens3_r1, lens3_r2)[0]

#print(lens3_r1_)
# r1 = []
# r2 = []
# cf = []
# coddingtonFactor = -1
# cf.append(-1)
# r1.append(17)
# r2.append(-17)
# n = 0.51358

# for i in range(100):
  #  coddingtonFactor += 0.001
  #  LensBend = cBending(coddingtonFactor, n, r1[i], r2[i])
  #  cf.append(coddingtonFactor)
#    r1.append(LensBend[0])
  #  r2.append(LensBend[1])

# print(cf)
# print(r1)
# print(r2)


# plt.plot(cf, r1, 'ro')
# plt.plot(cf, r2, 'gx')
# plt.show()
