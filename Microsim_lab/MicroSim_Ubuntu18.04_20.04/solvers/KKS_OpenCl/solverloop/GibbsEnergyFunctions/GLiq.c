/******************************************************************************
 *                       Code generated with sympy 1.8                        *
 *                                                                            *
 *              See http://www.sympy.org/ for more information.               *
 *                                                                            *
 *                       This file is part of 'project'                       *
 ******************************************************************************/
#include "GLiq.h"
//#include <math.h>

void GEL(double T, double *y, double *GEL) {

   (*GEL) = 8.3145000000000007*T*(1.0*((y[0] > 1.0000000000000001e-15) ? (
      log(y[0])*y[0]
   )
   : (
      0
   )) + 1.0*((y[1] > 1.0000000000000001e-15) ? (
      log(y[1])*y[1]
   )
   : (
      0
   )))/(1.0*y[0] + 1.0*y[1]) + (((T >= 298.14999999999998 && T < 1728.0) ? (
      -3.8231800000000003e-21*pow(T, 7) - 0.0048406999999999999*pow(T, 2) - 22.096*T*log(T) + 108.45699999999999*T + 11235.527
   )
   : ((T >= 1728.0 && T < 3000.0) ? (
      -43.100000000000001*T*log(T) + 268.59800000000001*T - 9549.7749999999996
   )
   : (
      0
   )))*y[1] + ((T >= 298.14999999999998 && T < 2750.0) ? (
      -3.0609799999999999e-23*pow(T, 7) - 3.5011899999999999e-7*pow(T, 3) + 0.000203475*pow(T, 2) - 26.4711*T*log(T) + 131.22905700000001*T + 21262.202000000001 + 93399/T
   )
   : ((T >= 2750.0 && T < 6000.0) ? (
      -41.770000000000003*T*log(T) + 260.756148*T - 7499.3980000000001
   )
   : (
      0
   )))*y[0])/(1.0*y[0] + 1.0*y[1]) + ((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[0]*y[1] + (-6.3149800000000003*T - 80037.300000000003)*y[0]*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[0]*y[1])/(1.0*y[0] + 1.0*y[1]);

}

void dGEL(double T, double *y, double *dGEL) {

   dGEL[0] = -8.3145000000000007*T*(1.0*((y[0] > 1.0000000000000001e-15) ? (
      log(y[0])*y[0]
   )
   : (
      0
   )) + 1.0*((y[1] > 1.0000000000000001e-15) ? (
      log(y[1])*y[1]
   )
   : (
      0
   )))/pow(1.0*y[0] + 1.0*y[1], 2) + 8.3145000000000007*T*((y[0] > 1.0000000000000001e-15) ? (
      log(y[0]) + 1
   )
   : (
      0
   ))/(1.0*y[0] + 1.0*y[1]) - 1.0*(((T >= 298.14999999999998 && T < 1728.0) ? (
      -3.8231800000000003e-21*pow(T, 7) - 0.0048406999999999999*pow(T, 2) - 22.096*T*log(T) + 108.45699999999999*T + 11235.527
   )
   : ((T >= 1728.0 && T < 3000.0) ? (
      -43.100000000000001*T*log(T) + 268.59800000000001*T - 9549.7749999999996
   )
   : (
      0
   )))*y[1] + ((T >= 298.14999999999998 && T < 2750.0) ? (
      -3.0609799999999999e-23*pow(T, 7) - 3.5011899999999999e-7*pow(T, 3) + 0.000203475*pow(T, 2) - 26.4711*T*log(T) + 131.22905700000001*T + 21262.202000000001 + 93399/T
   )
   : ((T >= 2750.0 && T < 6000.0) ? (
      -41.770000000000003*T*log(T) + 260.756148*T - 7499.3980000000001
   )
   : (
      0
   )))*y[0])/pow(1.0*y[0] + 1.0*y[1], 2) + ((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[1] + (97884.899999999994 - 19.01069*T)*y[0]*y[1] + (-6.3149800000000003*T - 80037.300000000003)*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[1] + (20000.0*y[0] - 20000.0*y[1])*y[0]*y[1])/(1.0*y[0] + 1.0*y[1]) + ((T >= 298.14999999999998 && T < 2750.0) ? (
      -3.0609799999999999e-23*pow(T, 7) - 3.5011899999999999e-7*pow(T, 3) + 0.000203475*pow(T, 2) - 26.4711*T*log(T) + 131.22905700000001*T + 21262.202000000001 + 93399/T
   )
   : ((T >= 2750.0 && T < 6000.0) ? (
      -41.770000000000003*T*log(T) + 260.756148*T - 7499.3980000000001
   )
   : (
      0
   )))/(1.0*y[0] + 1.0*y[1]) - 1.0*((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[0]*y[1] + (-6.3149800000000003*T - 80037.300000000003)*y[0]*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[0]*y[1])/pow(1.0*y[0] + 1.0*y[1], 2);
   dGEL[1] = -8.3145000000000007*T*(1.0*((y[0] > 1.0000000000000001e-15) ? (
      log(y[0])*y[0]
   )
   : (
      0
   )) + 1.0*((y[1] > 1.0000000000000001e-15) ? (
      log(y[1])*y[1]
   )
   : (
      0
   )))/pow(1.0*y[0] + 1.0*y[1], 2) + 8.3145000000000007*T*((y[1] > 1.0000000000000001e-15) ? (
      log(y[1]) + 1
   )
   : (
      0
   ))/(1.0*y[0] + 1.0*y[1]) - 1.0*(((T >= 298.14999999999998 && T < 1728.0) ? (
      -3.8231800000000003e-21*pow(T, 7) - 0.0048406999999999999*pow(T, 2) - 22.096*T*log(T) + 108.45699999999999*T + 11235.527
   )
   : ((T >= 1728.0 && T < 3000.0) ? (
      -43.100000000000001*T*log(T) + 268.59800000000001*T - 9549.7749999999996
   )
   : (
      0
   )))*y[1] + ((T >= 298.14999999999998 && T < 2750.0) ? (
      -3.0609799999999999e-23*pow(T, 7) - 3.5011899999999999e-7*pow(T, 3) + 0.000203475*pow(T, 2) - 26.4711*T*log(T) + 131.22905700000001*T + 21262.202000000001 + 93399/T
   )
   : ((T >= 2750.0 && T < 6000.0) ? (
      -41.770000000000003*T*log(T) + 260.756148*T - 7499.3980000000001
   )
   : (
      0
   )))*y[0])/pow(1.0*y[0] + 1.0*y[1], 2) + ((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[0] + (-6.3149800000000003*T - 80037.300000000003)*y[0] + (19.01069*T - 97884.899999999994)*y[0]*y[1] + (-20000.0*y[0] + 20000.0*y[1])*y[0]*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[0])/(1.0*y[0] + 1.0*y[1]) + ((T >= 298.14999999999998 && T < 1728.0) ? (
      -3.8231800000000003e-21*pow(T, 7) - 0.0048406999999999999*pow(T, 2) - 22.096*T*log(T) + 108.45699999999999*T + 11235.527
   )
   : ((T >= 1728.0 && T < 3000.0) ? (
      -43.100000000000001*T*log(T) + 268.59800000000001*T - 9549.7749999999996
   )
   : (
      0
   )))/(1.0*y[0] + 1.0*y[1]) - 1.0*((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[0]*y[1] + (-6.3149800000000003*T - 80037.300000000003)*y[0]*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[0]*y[1])/pow(1.0*y[0] + 1.0*y[1], 2);

}

void ddGEL(double T, double *y, double *ddGEL) {

   ddGEL[0] = 8.3145000000000007*T*((y[0] > 1.0000000000000001e-15) ? (
      1.0/y[0]
   )
   : (
      0
   ))/(1.0*y[0] + 1.0*y[1]) - 8.3145000000000007*T*((y[0] > 1.0000000000000001e-15) ? (
      log(y[0]) + 1
   )
   : (
      0
   ))/pow(1.0*y[0] + 1.0*y[1], 2) + 8.3145000000000007*T*((y[1] > 1.0000000000000001e-15) ? (
      log(y[1]) + 1
   )
   : (
      0
   ))/pow(1.0*y[0] + 1.0*y[1], 2) + (2*(97884.899999999994 - 19.01069*T)*y[1] + 2*(20000.0*y[0] - 20000.0*y[1])*y[1] + 20000.0*y[0]*y[1])/(1.0*y[0] + 1.0*y[1]) - (-6.3149800000000003*T + (97884.899999999994 - 19.01069*T)*(y[0] - y[1]) + (97884.899999999994 - 19.01069*T)*y[0] + (19.01069*T - 97884.899999999994)*y[1] + (-20000.0*y[0] + 20000.0*y[1])*y[1] + 10000.0*pow(y[0] - y[1], 2) + (20000.0*y[0] - 20000.0*y[1])*y[0] - 20000.0*y[0]*y[1] - 80037.300000000003)/(1.0*y[0] + 1.0*y[1]) + 1.0*((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[0] + (-6.3149800000000003*T - 80037.300000000003)*y[0] + (19.01069*T - 97884.899999999994)*y[0]*y[1] + (-20000.0*y[0] + 20000.0*y[1])*y[0]*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[0])/pow(1.0*y[0] + 1.0*y[1], 2) - 1.0*((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[1] + (97884.899999999994 - 19.01069*T)*y[0]*y[1] + (-6.3149800000000003*T - 80037.300000000003)*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[1] + (20000.0*y[0] - 20000.0*y[1])*y[0]*y[1])/pow(1.0*y[0] + 1.0*y[1], 2) + 1.0*((T >= 298.14999999999998 && T < 1728.0) ? (
      -3.8231800000000003e-21*pow(T, 7) - 0.0048406999999999999*pow(T, 2) - 22.096*T*log(T) + 108.45699999999999*T + 11235.527
   )
   : ((T >= 1728.0 && T < 3000.0) ? (
      -43.100000000000001*T*log(T) + 268.59800000000001*T - 9549.7749999999996
   )
   : (
      0
   )))/pow(1.0*y[0] + 1.0*y[1], 2) - 1.0*((T >= 298.14999999999998 && T < 2750.0) ? (
      -3.0609799999999999e-23*pow(T, 7) - 3.5011899999999999e-7*pow(T, 3) + 0.000203475*pow(T, 2) - 26.4711*T*log(T) + 131.22905700000001*T + 21262.202000000001 + 93399/T
   )
   : ((T >= 2750.0 && T < 6000.0) ? (
      -41.770000000000003*T*log(T) + 260.756148*T - 7499.3980000000001
   )
   : (
      0
   )))/pow(1.0*y[0] + 1.0*y[1], 2);
   ddGEL[1] = -8.3145000000000007*T*((y[1] > 1.0000000000000001e-15) ? (
      1.0/y[1]
   )
   : (
      0
   ))/(1.0*y[0] + 1.0*y[1]) - 8.3145000000000007*T*((y[0] > 1.0000000000000001e-15) ? (
      log(y[0]) + 1
   )
   : (
      0
   ))/pow(1.0*y[0] + 1.0*y[1], 2) + 8.3145000000000007*T*((y[1] > 1.0000000000000001e-15) ? (
      log(y[1]) + 1
   )
   : (
      0
   ))/pow(1.0*y[0] + 1.0*y[1], 2) - (2*(19.01069*T - 97884.899999999994)*y[0] + 2*(-20000.0*y[0] + 20000.0*y[1])*y[0] + 20000.0*y[0]*y[1])/(1.0*y[0] + 1.0*y[1]) + (-6.3149800000000003*T + (97884.899999999994 - 19.01069*T)*(y[0] - y[1]) + (97884.899999999994 - 19.01069*T)*y[0] + (19.01069*T - 97884.899999999994)*y[1] + (-20000.0*y[0] + 20000.0*y[1])*y[1] + 10000.0*pow(y[0] - y[1], 2) + (20000.0*y[0] - 20000.0*y[1])*y[0] - 20000.0*y[0]*y[1] - 80037.300000000003)/(1.0*y[0] + 1.0*y[1]) + 1.0*((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[0] + (-6.3149800000000003*T - 80037.300000000003)*y[0] + (19.01069*T - 97884.899999999994)*y[0]*y[1] + (-20000.0*y[0] + 20000.0*y[1])*y[0]*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[0])/pow(1.0*y[0] + 1.0*y[1], 2) - 1.0*((97884.899999999994 - 19.01069*T)*(y[0] - y[1])*y[1] + (97884.899999999994 - 19.01069*T)*y[0]*y[1] + (-6.3149800000000003*T - 80037.300000000003)*y[1] + 10000.0*pow(y[0] - y[1], 2)*y[1] + (20000.0*y[0] - 20000.0*y[1])*y[0]*y[1])/pow(1.0*y[0] + 1.0*y[1], 2) + 1.0*((T >= 298.14999999999998 && T < 1728.0) ? (
      -3.8231800000000003e-21*pow(T, 7) - 0.0048406999999999999*pow(T, 2) - 22.096*T*log(T) + 108.45699999999999*T + 11235.527
   )
   : ((T >= 1728.0 && T < 3000.0) ? (
      -43.100000000000001*T*log(T) + 268.59800000000001*T - 9549.7749999999996
   )
   : (
      0
   )))/pow(1.0*y[0] + 1.0*y[1], 2) - 1.0*((T >= 298.14999999999998 && T < 2750.0) ? (
      -3.0609799999999999e-23*pow(T, 7) - 3.5011899999999999e-7*pow(T, 3) + 0.000203475*pow(T, 2) - 26.4711*T*log(T) + 131.22905700000001*T + 21262.202000000001 + 93399/T
   )
   : ((T >= 2750.0 && T < 6000.0) ? (
      -41.770000000000003*T*log(T) + 260.756148*T - 7499.3980000000001
   )
   : (
      0
   )))/pow(1.0*y[0] + 1.0*y[1], 2);

}