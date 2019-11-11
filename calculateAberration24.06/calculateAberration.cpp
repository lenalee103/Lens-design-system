#ifdef __cplusplus
        extern "C"
		{
			__declspec(dllexport) double calculateW040for3Lenses(double wavelength, double h, double d1, double d2, 
			double lens1_r1, double lens1_r2, double lens1_n, double lens1_t, 
			double lens2_r1, double lens2_r2, double lens2_n, double lens2_t,
			double lens3_r1, double lens3_r2, double lens3_n, double lens3_t);
		};
#endif

/**
* @brief Trace the paraxial ray of the marginal ray.
*
* The main idea is descriped in the book "Introduction to Lens Design with Practical
* ZEMAX Examples" by Joseph M. Geary, First Printing, Sep 2002. 
* The calculation of the terms y, u and u_dash (page 108) is implemented here.
* This function will be used in @see calculateW040for3Lenses
*
* @param[in] h 		height of the incoming ray
* @param[in] alpha 	angle of the incoming ray
* @param[in] d 		distance between start of the incoming ray to the lens
* @param[in] r1 	front radius of the lens
* @param[in] r2		back radius of the lens
* @param[in] n 		refractive index of the lens
* @param[in] t		thickness of the lens
*
* @param[out] y1	height of ray before the first refraction
* @param[out] u1	angle of ray before the first refraction
* @param[out] u_dash1	angle of ray after the first refraction
*
* @param[out] y2	height of ray before the second refraction
* @param[out] u2	height of ray before the second refraction
* @param[out] u_dash2	height of ray after the second refraction
*
* @date 18.06.2018
* @see calculateW040for3Lenses
*/

void paraxialRayTrace(double h, double alpha, double d, double r1, double r2, double n, double t,
                      double &y1, double &u1, double &u_dash1, double &y2, double &u2, double &u_dash2)
{
    double n_air = 1.0; // Refractive index of the air

    y1 		= h + alpha*d;
    u1 		= alpha;
    u_dash1 	= (n_air-n)/(r1*n)*y1 + (n_air/n)*u1;

    y2 		= y1 + u_dash1*t;
    u2 		= u_dash1;
    u_dash2 	= ((n-n_air)/(r2*n_air))*y2 + (n/n_air)*u2;
}

/**
* @brief Calculates the S040 over one surface.
*
* The main idea is descriped in the book "Introduction to Lens Design with Practical
* ZEMAX Examples" by Joseph M. Geary, First Printing, Sep 2002. 
* The calculation of S040 for one surface via Paraxial Ray Trace 
* (page 105-109) is implementated here. 
* This function will be used in @see calculateW040for3Lenses
*
* @param[in] y		height of the incomming ray
* @param[in] u		angle of ray before refraction
* @param[in] u_dash	angle of ray after refraction
* @param[in] r 		surface radius
* @param[in] n1 	refractive index in front of the surface
* @param[in] n2 	refractive index behind the surface
*
* @date 18.06.2018
* @see calculateW040for3Lenses
*/
double calculateS040(double y, double u, double u_dash, double r, double n1, double n2)
{
    double C 		= 1.0/r;
    double A 		= n1*(u + y*C);
    double deltaL 	= (u_dash/n2) - (u/n1);
    double S040		= -1.0 * A*A*y*deltaL;

    return S040;
}

/**
* @brief Calculates the aberration by W040 criteria for 3 lenses. 
*
* The main idea is descriped in the book "Introduction to Lens Design with Practical
* ZEMAX Examples" by Joseph M. Geary, First Printing, Sep 2002. 
* The calculation of W040 for 3 Lenses via Paraxial Ray Trace 
* (page 107-109) is implementated here. 
*
* @param wavelength 	wavelength of the incoming ray
* @param h 		the high of the input beam (input beam diameter)
* @param d1		distance from first to second lens
* @param d2		distance from second to third lens
'
* @param lens1_r1       front radius of the first lens
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
* @date 18.06.2018
* @see calculateS040
* @see paraxialRayTrace
*/
double calculateW040for3Lenses(double wavelength, double h, double d1, double d2, 
                               double lens1_r1, double lens1_r2, double lens1_n, double lens1_t,
                               double lens2_r1, double lens2_r2, double lens2_n, double lens2_t,
                               double lens3_r1, double lens3_r2, double lens3_n, double lens3_t)
{
	double n_air = 1.0; // Refractive index of the air
    double S040 = 0;
    double y1, u1, u_dash1, y2, u2, u_dash2;
	
	// First Lense
    paraxialRayTrace(h, 0, 10, lens1_r1, lens1_r2, lens1_n, lens1_t, y1, u1, u_dash1, y2, u2, u_dash2);
    S040 += calculateS040(y1, u1, u_dash1, lens1_r1, n_air  , lens1_n);
    S040 += calculateS040(y2, u2, u_dash2, lens1_r2, lens1_n, n_air  );

	// Second Lense
    paraxialRayTrace(y2, u_dash2, d1, lens2_r1, lens2_r2, lens2_n, lens2_t, y1, u1, u_dash1, y2, u2, u_dash2);
    S040 += calculateS040(y1, u1, u_dash1, lens2_r1, n_air  , lens2_n);
    S040 += calculateS040(y2, u2, u_dash2, lens2_r2, lens2_n, n_air  );

	// Third Lense
    paraxialRayTrace(y2, u_dash2, d2, lens3_r1, lens3_r2, lens3_n, lens3_t, y1, u1, u_dash1, y2, u2, u_dash2);
    S040 += calculateS040(y1, u1, u_dash1, lens3_r1, n_air  , lens3_n);
    S040 += calculateS040(y2, u2, u_dash2, lens3_r2, lens3_n, n_air  );

	// Calculating W040 considering the wavelength
    double W040 = S040*0.125*1000.0/wavelength;

    return W040;
}

#include <iostream>
#include <cmath> 

/**
* Tests all functions inside of Tracy, which are necessary.
* @return returns true, if all tests are successful, 
*/
bool unitTests_Tracy()
{
	bool tests_successful = true;
	
	double h = 4;
	double alpha = 0;
	double d = 10;
	double r1 = 1/0.044504;
	double r2 = 1e12;
	double n = 1.458;
	double t = 1.381;
	
	double y1, u1, u_dash1, y2, u2, u_dash2;
	paraxialRayTrace(h, alpha, d, r1, r2, n, t, y1, u1, u_dash1, y2, u2, u_dash2);
	
	if( std::abs(y1-4 + u1-0 + u_dash1+0.05592 + y2-3.922774 + u2+0.05592 + u_dash2+0.081531) < 0.0001)
	{
		std::cout << "1. Test -- paraxialRayTrace -----------------> successful" << std::endl;
	} else 
	{
		std::cout << "1. Test -- paraxialRayTrace -----------------> failed" <<  std::endl;
		std::cout << "   ---------> !! Warning !! CalculateS040 only works if paraxialRayTrace do not fail" <<  std::endl;
		tests_successful = false;
	}
	
	double S404 = calculateS040(y2, u2, u_dash2, r2, n, 1);
	if( std::abs(S404 - 0.001126) < 0.0001 ) 
	{
		std::cout << "2. Test -- calculateS040 --------------------> successful" <<  std::endl;
	} else 
	{
		std::cout << "2. Test -- calculateS040 --------------------> failed" <<  std::endl;
		tests_successful = false;
	}
	
	double wavelength = 1.064;
    h  = 2;
    double d1 = 17.0197423589288;
    double d2 = 7.74878708722231;

    double lens1_r1 = 29.52;
    double lens1_r2 = -29.52;
    double lens1_n = 1.50663348492911;
    double lens1_t = 7.74;

    double lens2_r1 = -7;
    double lens2_r2 = 1e+12;
    double lens2_n = 1.75389272961219;
    double lens2_t = 2;

    double lens3_r1 = 38.6;
    double lens3_r2 = 1e+12;
    double lens3_n = 1.50663348492911;
    double lens3_t = 4.1;

    double target_W040 = 0.033737;
	double W040;
	
    W040 = calculateW040for3Lenses(wavelength, h, d1, d2,
                                   lens1_r1, lens1_r2, lens1_n, lens1_t,
                                   lens2_r1, lens2_r2, lens2_n, lens2_t,
                                   lens3_r1, lens3_r2, lens3_n, lens3_t);

	if( std::abs(W040 - target_W040) < 0.0001 ) 
	{
		std::cout << "3. Test -- calculateW040for3Lenses ----------> successful" <<  std::endl;
	} else 
	{
		std::cout << "3. Test -- calculateW040for3Lenses ----------> failed" <<  std::endl;
		tests_successful = false;
	}
	
	return tests_successful;
}

int main()
{
    unitTests_Tracy();
    return 0;
}




