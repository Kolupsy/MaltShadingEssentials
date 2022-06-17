
#ifndef SHADINGESSENTIALS_VECTORMATH_GLSL
#define SHADINGESSENTIALS_VECTORMATH_GLSL

#include "Math.glsl"

/* META @meta: internal=true; */
void vector_math_add(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = a + b;
}

/* META @meta: internal=true; */
void vector_math_subtract(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = a - b;
}

/* META @meta: internal=true; */
void vector_math_multiply(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = a * b;
}

/* META @meta: internal=true; */
void vector_math_divide(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = vec3_divide(a, b);
}

/* META @meta: internal=true; */
void vector_math_cross(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = cross(a, b);
}

/* META @meta: internal=true; */
void vector_math_project(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  float lenSquared = dot(b, b);
  outVector = (lenSquared != 0.0) ? (dot(a, b) / lenSquared) * b : vec3(0.0);
}

/* META @meta: internal=true; */
void vector_math_reflect(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = reflect(a, normalize(b));
}

/* META @meta: internal=true; */
void vector_math_dot(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outValue = dot(a, b);
}

/* META @meta: internal=true; */
void vector_math_distance(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outValue = distance(a, b);
}

/* META @meta: internal=true; */
void vector_math_length(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outValue = length(a);
}

/* META @meta: internal=true; */
void vector_math_scale(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = a * scale;
}

/* META @meta: internal=true; */
void vector_math_normalize(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = a;
  /* Safe version of normalize(a). */
  float lenSquared = dot(a, a);
  if (lenSquared > 0.0) {
    outVector *= inversesqrt(lenSquared);
  }
}

/* META @meta: internal=true; */
void vector_math_snap(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = floor(vec3_divide(a, b)) * b;
}

/* META @meta: internal=true; */
void vector_math_floor(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = floor(a);
}

/* META @meta: internal=true; */
void vector_math_ceil(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = ceil(a);
}

/* META @meta: internal=true; */
void vector_math_modulo(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = modf(a, b);
}

// float wrap( float a, float b, float c ){
//   float range = c - b;
//   return ( range <= 0 ) ? b : a - ( range * floor(( a - b ) / range ));
// }

/* META @meta: internal=true; */
void vector_math_wrap(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = vec3( 0 );
  math_wrap( a.x, b.x, c.x, outVector.x );
  math_wrap( a.y, b.y, c.y, outVector.y );
  math_wrap( a.z, b.z, c.z, outVector.z );
}

/* META @meta: internal=true; */
void vector_math_fraction(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = fract(a);
}

/* META @meta: internal=true; */
void vector_math_absolute(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = abs(a);
}

/* META @meta: internal=true; */
void vector_math_minimum(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = min(a, b);
}

/* META @meta: internal=true; */
void vector_math_maximum(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = max(a, b);
}

/* META @meta: internal=true; */
void vector_math_sine(vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = sin(a);
}

/* META @meta: internal=true; */
void vector_math_cosine(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = cos(a);
}

/* META @meta: internal=true; */
void vector_math_tangent(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = tan(a);
}

/* META @meta: internal=true; */
void vector_math_refract(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = refract(a, normalize(b), scale);
}

/* META @meta: internal=true; */
void vector_math_faceforward(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = faceforward(a, b, c);
}

/* META @meta: internal=true; */
void vector_math_multiply_add(
    vec3 a, vec3 b, vec3 c, float scale, out vec3 outVector, out float outValue)
{
  outVector = a * b + c;
}

#endif
