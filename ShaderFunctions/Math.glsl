#ifndef SHADINGESSENTIALS_MATH_GLSL
#define SHADINGESSENTIALS_MATH_GLSL

#include "Node Utils/float.glsl"

/* META @meta: internal=true; */
void math_add(float a, float b, float c, out float result)
{
  result = a + b;
}

/* META @meta: internal=true; */
void math_subtract(float a, float b, float c, out float result)
{
  result = a - b;
}

/* META @meta: internal=true; */
void math_multiply(float a, float b, float c, out float result)
{
  result = a * b;
}

/* META @meta: internal=true; */
void math_divide(float a, float b, float c, out float result)
{
  result = float_divide(a, b);
}

/* META @meta: internal=true; */
void math_power(float a, float b, float c, out float result)
{
  if (a >= 0.0) {
    result = float_pow(a, b);
  }
  else {
    float fraction = mod(abs(b), 1.0);
    if (fraction > 0.999 || fraction < 0.001) {
      result = float_pow(a, floor(b + 0.5));
    }
    else {
      result = 0.0;
    }
  }
}

/* META @meta: internal=true; */
void math_logarithm(float a, float b, float c, out float result)
{
  result = (a > 0.0 && b > 0.0) ? log2(a) / log2(b) : 0.0;
}

/* META @meta: internal=true; */
void math_sqrt(float a, float b, float c, out float result)
{
  result = (a > 0.0) ? sqrt(a) : 0.0;
}

/* META @meta: internal=true; */
void math_inversesqrt(float a, float b, float c, out float result)
{
  result = inversesqrt(a);
}

/* META @meta: internal=true; */
void math_absolute(float a, float b, float c, out float result)
{
  result = abs(a);
}

/* META @meta: internal=true; */
void math_radians(float a, float b, float c, out float result)
{
  result = radians(a);
}

/* META @meta: internal=true; */
void math_degrees(float a, float b, float c, out float result)
{
  result = degrees(a);
}

/* META @meta: internal=true; */
void math_minimum(float a, float b, float c, out float result)
{
  result = min(a, b);
}

/* META @meta: internal=true; */
void math_maximum(float a, float b, float c, out float result)
{
  result = max(a, b);
}

/* META @meta: internal=true; */
void math_less_than(float a, float b, float c, out float result)
{
  result = (a < b) ? 1.0 : 0.0;
}

/* META @meta: internal=true; */
void math_greater_than(float a, float b, float c, out float result)
{
  result = (a > b) ? 1.0 : 0.0;
}

/* META @meta: internal=true; */
void math_round(float a, float b, float c, out float result)
{
  result = floor(a + 0.5);
}

/* META @meta: internal=true; */
void math_floor(float a, float b, float c, out float result)
{
  result = floor(a);
}

/* META @meta: internal=true; */
void math_ceil(float a, float b, float c, out float result)
{
  result = ceil(a);
}

/* META @meta: internal=true; */
void math_fraction(float a, float b, float c, out float result)
{
  result = a - floor(a);
}

/* META @meta: internal=true; */
void math_modulo(float a, float b, float c, out float result)
{
  result = modf(a, b);
}

/* META @meta: internal=true; */
void math_trunc(float a, float b, float c, out float result)
{
  result = trunc(a);
}

/* META @meta: internal=true; */
void math_snap(float a, float b, float c, out float result)
{
  result = floor(float_divide(a, b)) * b;
}

/* META @meta: internal=true; */
void math_pingpong(float a, float b, float c, out float result)
{
  result = (b != 0.0) ? abs(fract((a - b) / (b * 2.0)) * b * 2.0 - b) : 0.0;
}

/* Adapted from godotengine math_funcs.h. */
/* META @meta: internal=true; */
void math_wrap(float a, float b, float c, out float result)
{
  float range = c - b;
    result = ( range <= 0 ) ? b : a - ( range * floor(( a - b ) / range ));
}

/* META @meta: internal=true; */
void math_sine(float a, float b, float c, out float result)
{
  result = sin(a);
}

/* META @meta: internal=true; */
void math_cosine(float a, float b, float c, out float result)
{
  result = cos(a);
}

/* META @meta: internal=true; */
void math_tangent(float a, float b, float c, out float result)
{
  result = tan(a);
}

/* META @meta: internal=true; */
void math_sinh(float a, float b, float c, out float result)
{
  result = sinh(a);
}

/* META @meta: internal=true; */
void math_cosh(float a, float b, float c, out float result)
{
  result = cosh(a);
}

/* META @meta: internal=true; */
void math_tanh(float a, float b, float c, out float result)
{
  result = tanh(a);
}

/* META @meta: internal=true; */
void math_arcsine(float a, float b, float c, out float result)
{
  result = (a <= 1.0 && a >= -1.0) ? asin(a) : 0.0;
}

/* META @meta: internal=true; */
void math_arccosine(float a, float b, float c, out float result)
{
  result = (a <= 1.0 && a >= -1.0) ? acos(a) : 0.0;
}

/* META @meta: internal=true; */
void math_arctangent(float a, float b, float c, out float result)
{
  result = atan(a);
}

/* META @meta: internal=true; */
void math_arctan2(float a, float b, float c, out float result)
{
  result = atan(a, b);
}

/* META @meta: internal=true; */
void math_sign(float a, float b, float c, out float result)
{
  result = sign(a);
}

/* META @meta: internal=true; */
void math_exponent(float a, float b, float c, out float result)
{
  result = exp(a);
}

/* META @meta: internal=true; */
void math_compare(float a, float b, float c, out float result)
{
  result = (abs(a - b) <= max(c, 1e-5)) ? 1.0 : 0.0;
}

/* META @meta: internal=true; */
void math_multiply_add(float a, float b, float c, out float result)
{
  result = a * b + c;
}

/* See: https://www.iquilezles.org/www/articles/smin/smin.htm. */
/* META @meta: internal=true; */
void math_smoothmin(float a, float b, float c, out float result)
{
  if (c != 0.0) {
    float h = max(c - abs(a - b), 0.0) / c;
    result = min(a, b) - h * h * h * c * (1.0 / 6.0);
  }
  else {
    result = min(a, b);
  }
}

/* META @meta: internal=true; */
void math_smoothmax(float a, float b, float c, out float result)
{
  math_smoothmin(-a, -b, c, result);
  result = -result;
}

#endif
