# compiling c++ function to a .dll file for python 
# use the keyword " extern "C" " at the beginning of your C++ file

#ifdef __cplusplus
	extern "C"
#endif
double foo(double a, double b) 
{
	your_code [...]
}

g++ -Wall cppFunktion.cpp -shared -o cppFunktion.dll

##########################################################

# using .dll file in python by using ctypes 

from ctypes import *
import os
path = 'U:/Tracy'	# path to .dll file
os.chdir(path)

cfoo = cdll.LoadLibrary('./calculateAberration.dll').calculateW040for3Lenses	# create function calculateW040for3Lenses
cfoo.argtypes = [c_double, c_double, etc.] 				# arguments types
cfoo.restype = c_double              						# return type, or None if void

cfoo(3,2, etc)

##########################################################