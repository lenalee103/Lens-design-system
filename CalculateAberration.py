from ctypes import *
import os
path = 'C:/Users/rf613258\Desktop/brain_and_b1\calculateAberration24.06'    	# path to .dll file
os.chdir(path)

cfunc = cdll.LoadLibrary('./calculateAberration.dll').calculateW040for3Lenses
cfunc.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double] 				# arguments types
cfunc.restype = c_double              						# return type, or None if void

# Customer defining parameters (Test Data from cpp)
wavelength = 1.064
h = 2
d1 = 17.0197423589288
d2 = 7.74878708722231
# d1 & d2 can be calculated by Cailing's cpp file.

# Initial parameters:
lens1_r1 = 29.52
lens1_r2 = -29.52
lens1_n = 1.50663348492911
lens1_t = 7.74

lens2_r1 = -7
lens2_r2 = 1e+12
lens2_n = 1.75389272961219
lens2_t = 2

lens3_r1 = 38.6
lens3_r2 = 1e+12
lens3_n = 1.50663348492911
lens3_t = 4.1

# print(cfunc(wavelength, h, d1, d2, lens1_r1, lens1_r2, lens1_n, lens1_t, lens2_r1, lens2_r2, lens2_n, lens2_t, lens3_r1, lens3_r2, lens3_n, lens3_t))


