#ifdef __cplusplus
        extern "C"
		{
			__declspec(dllexport) double* bendLens(double coddingtonFactor, double n, double r1, double r2);
		};
#endif

#include <iostream>
/**
* @brief Calculates the new radius after bending a lens with the factor "coddingtonFactor".
* 
* The calculation of the Coddington-Factor depents on the formular cf = (r2+r1)/(r2-r1).
* The calculation for the focus depents on 1/f = (n-1)*(1/r1 - 1/r2).
* After bending the lens the focus of the lens remains the same as before. 
*
* @param coddingtonFactor The Coddington Factor for the bending.
* @param n Reflactive Index of the lens.
* @param r1 Radius at the front of the lens.
* @param r2 Radius at the back of the lens.
*
* @return r_new The new radius of the lens after the bending. r_new[0] remains the radius
* at the front, while r_new[1] is the radius at the back of the lens.
*/
double* bendLens(double coddingtonFactor, double n, double r1, double r2)
{
	double* r_new = new double[2];
	double focus = (n-1) * (1/r1 - 1/r2);

	r_new[0] = (n-1)/focus * (1-(coddingtonFactor-1)/(coddingtonFactor+1));
	r_new[1] = r_new[0] * (coddingtonFactor+1)/(coddingtonFactor-1);

	return r_new;
}

// Small example
int main()
{
	double *r;
	double coddingtonFactor = 0.1;
	double r1 = 17;
	double r2 = -17; 
	double n = 0.51358;
	std::cout << "--- Original Lens ---" << std::endl;
	std::cout << "r1: " << r1 << std::endl;
	std::cout << "r2: " << r2 << std::endl << std::endl;

	std::cout << "--- Bended Lenses ---" << std::endl;
	for (int i=0 ; i<5; i++)
	{
		r = bendLens(coddingtonFactor, 0.51358, r1, r2);
		std::cout << "Bending factor: " <<  coddingtonFactor << std::endl;
		std::cout << "r1: " << r[0] << std::endl;
		std::cout << "r2: " << r[1] << std::endl << std::endl;
		coddingtonFactor += 0.1;
	}
}