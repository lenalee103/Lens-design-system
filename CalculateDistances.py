from ctypes import *
import os
path = 'C:/Users/rf613258\Desktop/brain_and_b1\calculateDistances'    	# path to .dll file
os.chdir(path)

cDistances = cdll.LoadLibrary('./calculateDistances.dll').calculateDistancesFor3Lenses
cDistances.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double,c_double, c_double] 				# arguments types
cDistances.restype = POINTER(c_double)     # return type, or None if void


h_in = 2.
h_out = 1.0 / 2.8 * 2.0

lens1_r1 = 29.52
lens1_r2 = -29.52
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

Distances = cDistances(h_in, h_out, lens1_r1, lens1_r2, lens1_n, lens1_t, lens2_r1, lens2_r2, lens2_n, lens2_t,
                       lens3_r1, lens3_r2, lens3_n, lens3_t)
# list = [Distances[i] for i in range(2)]

# print(list)
