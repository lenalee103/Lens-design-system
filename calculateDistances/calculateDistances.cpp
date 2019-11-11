#ifdef __cplusplus
        extern "C"
		{
			__declspec(dllexport) double* calculateDistancesFor3Lenses(double h_in, double h_out, 
            double lens1_r1, double lens1_r2, double lens1_n, double lens1_t,
            double lens2_r1, double lens2_r2, double lens2_n, double lens2_t,
            double lens3_r1, double lens3_r2, double lens3_n, double lens3_t);
		};
#endif

#include <cmath>
#include <iostream>

/**
* @brief Calculates the distance between the first and the second lens and
* between the second and third lens. 
*
* The main idea is to discribe the input ray as a vector v = (h, alpha)'. 
* In our case the angle alpha is always zero.
* For every translation of the ray v the translation matrix 
* ( 1  d )
* ( 0  1 )
* discribes the new ray after a distance of d.
* For a refraction at a surface the refraction matrix
* (        1           0     ) 
* ( (n1-n2)/(n2*r)   n1/n2   )
* discribes the new ray after the surface. Here n1 is the refrective index before
* and n2 after the surface.
* To calculate the distances d1 and d2 we obtain a system of non-linear equations
* with multiply translation and refraction matrices, where the input and output
* parameters are known, so that we can solve for the distances d1 and d2.
* The system of non-linear equations are already solved by hand with the ansatz 
* I*x + J*y + K*xy = A
* L*x + M*y + N*xy = B
*
* @param h_in 		the high of the input beam
* @param h_out 		the high of the output beam
*
* @param lens1_r1   front radius of the first lens
* @param lens1_r2	back radius of the first lens
* @param lens1_n	refractive index of the first lens
* @param lens1_t	thickness of the first lens
'
* @param lens2_r1	front radius of the first lens
* @param lens2_r2	back radius of the first lens
* @param lens2_n	refractive index of the first lens
* @param lens2_t	thickness of the first lens
*
* @param lens3_r1	front radius of the first lens
* @param lens3_r2	back radius of the first lens
* @param lens3_n	refractive index of the first lens
* @param lens3_t	thickness of the first lens
*
* @return distance distance[0] is the distance between first and second lens. 
*                  distance[0] is the distance between second and third lens.
* If NULL, than the system has no real solution. 
*
* @date 31.07.2018
*/
double* calculateDistancesFor3Lenses( double h_in, double h_out,double lens1_r1, double lens1_r2, double lens1_n, double lens1_t,
                                      double lens2_r1, double lens2_r2, double lens2_n, double lens2_t,
                                      double lens3_r1, double lens3_r2, double lens3_n, double lens3_t)
{
	double n_air = 1.0, P2 = 10., alpha_in = 0.;
	double C1, C2, C3, C4, C5, C6;
	
	if (lens1_r1 < 1e6) C1 = 1./lens1_r1;
	else C1 = 0.;
	
	if (lens1_r2 < 1e6) C2 = 1./lens1_r2;
	else C2 = 0.;
	
	if (lens2_r1 < 1e6) C3 = 1./lens2_r1;
	else C3 = 0.;
	
	if (lens2_r2 < 1e6) C4 = 1./lens2_r2;
	else C4 = 0.;
	
	if (lens3_r1 < 1e6) C5 = 1./lens3_r1;
	else C5 = 0.;
	
	if (lens3_r2 < 1e6) C6 = 1./lens3_r2;
	else C6 = 0.;
	
	double f1 = -( (lens1_n - n_air)/n_air*C2 + ( (lens1_n - n_air) / n_air*C2 * (n_air - lens1_n) / lens1_n * C1 * lens1_t ) + (lens1_n / n_air) * (n_air - lens1_n) / lens1_n * C1 );
	double f2 = -( (lens2_n - n_air)/n_air*C4 + ( (lens2_n - n_air) / n_air*C4 * (n_air - lens2_n) / lens2_n * C3 * lens2_t ) + (lens2_n / n_air) * (n_air - lens2_n) / lens2_n * C3 );
	double f3 = -( (lens3_n - n_air)/n_air*C6 + ( (lens3_n - n_air) / n_air*C6 * (n_air - lens3_n) / lens3_n * C5 * lens3_t ) + (lens3_n / n_air) * (n_air - lens3_n) / lens3_n * C5 );
	
	double a = 1. + (n_air - lens2_n)/lens2_n * C3 * lens2_t;
	double b = 1. + (n_air - lens1_n)/lens1_n * C1 * lens1_t;
	double c = lens2_t * n_air/lens2_n * f1;
	double d = 1. + (n_air - lens1_n)/lens1_n * C1 * lens1_t;
	double e = f1 * (1. + (lens2_n - n_air)/lens2_n * C4 * lens2_t);
	double f = 1. + (n_air - lens3_n)/lens3_n * C5 * lens3_t;
	double g = lens3_t * n_air/lens3_n;
	double h = 1. + (lens3_n - n_air)/lens3_n * C6 * lens3_t;

	double h_inConstantheight = h_in * (f * a * b - f * c - g * d * f2 - g * e);
	double h_inD1constantheight = h_in * (g * f2 * f1 - f * a * f1);
	double h_inD2constantheight = h_in * (-1. * f * d * f2 - f * e);
	double h_inD1D2constantheight = h_in * f * f2 * f1;
	double h_inConstantAngle = h_in * (-a * b * f3 + c * f3 - h * d * f2 - h * e);
	double h_inD1Angleconstant = h_in * (a * f3 * f1 + h * f1 * f2);
	double h_inD2Angleconstant = h_in * (d * f3 * f2 + e * f3);
	double h_inD1D2Angleconstant = h_in * (-1. * f3 * f2 * f1);

	double Propagationendh_inConstantAngle = P2 * h_in * (-a * b * f3 + c * f3 - h * d * f2 - h * e);
	double Propagationendh_inD1Angleconstant = P2 * h_in * (a * f3 * f1 + h * f1 * f2);
	double Propagationendh_inD2Angleconstant = P2 * h_in * (d * f3 * f2 + e * f3);
	double Propagationendh_inD1D2Angleconstant = -P2 * h_in * f3 * f2 * f1;
	
	double HeightConstplus = h_inConstantheight + Propagationendh_inConstantAngle;
	double HeightD1plus = h_inD1constantheight + Propagationendh_inD1Angleconstant;
	double HeightD2plus = h_inD2constantheight + Propagationendh_inD2Angleconstant;
	double HeightD1D2plus = h_inD1D2constantheight + Propagationendh_inD1D2Angleconstant;

	double A = h_out - HeightConstplus;
	double B = alpha_in - h_inConstantAngle;
	double I = HeightD1plus;
	double J = HeightD2plus;
	double K = HeightD1D2plus;
	double L = h_inD1Angleconstant;
	double M = h_inD2Angleconstant;
	double N = h_inD1D2Angleconstant;

	double AlphaDash = (I - ((K * L) / N));
	double BetaDash = (J - ((K * M) / (N)));
	double Gamma = -1. * AlphaDash * N * N;
	double Theta = BetaDash * N * L - M * N * AlphaDash + A * N * N - B * K * N;
	double Delta = M * A * N - M * B * K - BetaDash * B * N;
	
	double sqrtpart = Theta * Theta - 4.0 * Gamma * Delta;
	if (sqrtpart > 0)
	{
		double* distance = new double[2];
		distance[0] = (-Theta - std::sqrt(sqrtpart)) / (2.0 * Gamma);
		distance[1] = (B - (L * distance[0])) / (M + (N * distance[0]));
		return distance;
	}
	return NULL;
}

int main()
{
	// Test case for the distance calculation
	double h_in = 2.;
	double h_out = 1.0/2.8 *2.0;
	
    double lens1_r1 = 29.52;
    double lens1_r2 = -29.52;
    double lens1_n = 1.50663348492911;
    double lens1_t = 7.74;

    double lens2_r1 = -7.;
    double lens2_r2 = 1e+12;
    double lens2_n = 1.75389272961219;
    double lens2_t = 2.;

    double lens3_r1 = 38.6;
    double lens3_r2 = 1e+12;
    double lens3_n = 1.50663348492911;
    double lens3_t = 4.1; 
 
	double* d;
	d = calculateDistancesFor3Lenses(h_in, h_out, lens1_r1, lens1_r2, lens1_n, lens1_t, lens2_r1, lens2_r2,  lens2_n, lens2_t, lens3_r1, lens3_r2, lens3_n, lens3_t);
	
	//d1_soll = 17.1783;
	//d2_soll = 0.770647;
	std::cout << "d1: " << d[0] << std::endl;
	std::cout << "d2: " << d[1] << std::endl;
	
	return 0;
}