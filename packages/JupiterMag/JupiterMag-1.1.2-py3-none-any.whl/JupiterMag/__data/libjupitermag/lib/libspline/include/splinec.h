#ifndef __LIBSPLINE_H__
#define __LIBSPLINE_H__
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define LIBSPLINE_VERSION_MAJOR 0
#define LIBSPLINE_VERSION_MINOR 0
#define LIBSPLINE_VERSION_PATCH 1

#define _USE_MATH_DEFINES

void spline(int n0, double *x0, double *y0, 
			int n1, double *x1, double *y1);




#endif
