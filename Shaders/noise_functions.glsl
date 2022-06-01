#ifndef SHADINGESSENTIALS_NOISE_FUNCTIONS_GLSL
#define SHADINGESSENTIALS_NOISE_FUNCTIONS_GLSL

/* ***** Jenkins Lookup3 Hash Functions ***** */

/* Source: http://burtleburtle.net/bob/c/lookup3.c */

#define rot(x, k) (((x) << (k)) | ((x) >> (32 - (k))))

#define mix(a, b, c) \
  { \
    a -= c; \
    a ^= rot(c, 4); \
    c += b; \
    b -= a; \
    b ^= rot(a, 6); \
    a += c; \
    c -= b; \
    c ^= rot(b, 8); \
    b += a; \
    a -= c; \
    a ^= rot(c, 16); \
    c += b; \
    b -= a; \
    b ^= rot(a, 19); \
    a += c; \
    c -= b; \
    c ^= rot(b, 4); \
    b += a; \
  }

#define final(a, b, c) \
  { \
    c ^= b; \
    c -= rot(b, 14); \
    a ^= c; \
    a -= rot(c, 11); \
    b ^= a; \
    b -= rot(a, 25); \
    c ^= b; \
    c -= rot(b, 16); \
    a ^= c; \
    a -= rot(c, 4); \
    b ^= a; \
    b -= rot(a, 14); \
    c ^= b; \
    c -= rot(b, 24); \
  }

uint hash_uint(uint kx)
{
  uint a, b, c;
  a = b = c = 0xdeadbeefu + (1u << 2u) + 13u;

  a += kx;
  final(a, b, c);

  return c;
}

uint hash_uint2(uint kx, uint ky)
{
  uint a, b, c;
  a = b = c = 0xdeadbeefu + (2u << 2u) + 13u;

  b += ky;
  a += kx;
  final(a, b, c);

  return c;
}

uint hash_uint3(uint kx, uint ky, uint kz)
{
  uint a, b, c;
  a = b = c = 0xdeadbeefu + (3u << 2u) + 13u;

  c += kz;
  b += ky;
  a += kx;
  final(a, b, c);

  return c;
}

uint hash_uint4(uint kx, uint ky, uint kz, uint kw)
{
  uint a, b, c;
  a = b = c = 0xdeadbeefu + (4u << 2u) + 13u;

  a += kx;
  b += ky;
  c += kz;
  mix(a, b, c);

  a += kw;
  final(a, b, c);

  return c;
}

#undef rot
#undef final
#undef mix

uint hash_int(int kx)
{
  return hash_uint(uint(kx));
}

uint hash_int2(int kx, int ky)
{
  return hash_uint2(uint(kx), uint(ky));
}

uint hash_int3(int kx, int ky, int kz)
{
  return hash_uint3(uint(kx), uint(ky), uint(kz));
}

uint hash_int4(int kx, int ky, int kz, int kw)
{
  return hash_uint4(uint(kx), uint(ky), uint(kz), uint(kw));
}

/* Hashing uint or uint[234] into a float in the range [0, 1]. */

float hash_uint_to_float(uint kx)
{
  return float(hash_uint(kx)) / float(0xFFFFFFFFu);
}

float hash_uint2_to_float(uint kx, uint ky)
{
  return float(hash_uint2(kx, ky)) / float(0xFFFFFFFFu);
}

float hash_uint3_to_float(uint kx, uint ky, uint kz)
{
  return float(hash_uint3(kx, ky, kz)) / float(0xFFFFFFFFu);
}

float hash_uint4_to_float(uint kx, uint ky, uint kz, uint kw)
{
  return float(hash_uint4(kx, ky, kz, kw)) / float(0xFFFFFFFFu);
}

/* Hashing float or vec[234] into a float in the range [0, 1]. */

float hash_float_to_float(float k)
{
  return hash_uint_to_float(floatBitsToUint(k));
}

float hash_vec2_to_float(vec2 k)
{
  return hash_uint2_to_float(floatBitsToUint(k.x), floatBitsToUint(k.y));
}

float hash_vec3_to_float(vec3 k)
{
  return hash_uint3_to_float(floatBitsToUint(k.x), floatBitsToUint(k.y), floatBitsToUint(k.z));
}

float hash_vec4_to_float(vec4 k)
{
  return hash_uint4_to_float(
      floatBitsToUint(k.x), floatBitsToUint(k.y), floatBitsToUint(k.z), floatBitsToUint(k.w));
}

/* Hashing vec[234] into vec[234] of components in the range [0, 1]. */

vec2 hash_vec2_to_vec2(vec2 k)
{
  return vec2(hash_vec2_to_float(k), hash_vec3_to_float(vec3(k, 1.0)));
}

vec3 hash_vec3_to_vec3(vec3 k)
{
  return vec3(
      hash_vec3_to_float(k), hash_vec4_to_float(vec4(k, 1.0)), hash_vec4_to_float(vec4(k, 2.0)));
}

vec4 hash_vec4_to_vec4(vec4 k)
{
  return vec4(hash_vec4_to_float(k.xyzw),
              hash_vec4_to_float(k.wxyz),
              hash_vec4_to_float(k.zwxy),
              hash_vec4_to_float(k.yzwx));
}

/* Hashing float or vec[234] into vec3 of components in range [0, 1]. */

vec3 hash_float_to_vec3(float k)
{
  return vec3(
      hash_float_to_float(k), hash_vec2_to_float(vec2(k, 1.0)), hash_vec2_to_float(vec2(k, 2.0)));
}

vec3 hash_vec2_to_vec3(vec2 k)
{
  return vec3(
      hash_vec2_to_float(k), hash_vec3_to_float(vec3(k, 1.0)), hash_vec3_to_float(vec3(k, 2.0)));
}

vec3 hash_vec4_to_vec3(vec4 k)
{
  return vec3(hash_vec4_to_float(k.xyzw), hash_vec4_to_float(k.zxwy), hash_vec4_to_float(k.wzyx));
}

/* Other Hash Functions */

float integer_noise(int n)
{
  /* Integer bit-shifts for these calculations can cause precision problems on macOS.
   * Using uint resolves these issues. */
  uint nn;
  nn = (uint(n) + 1013u) & 0x7fffffffu;
  nn = (nn >> 13u) ^ nn;
  nn = (uint(nn * (nn * nn * 60493u + 19990303u)) + 1376312589u) & 0x7fffffffu;
  return 0.5 * (float(nn) / 1073741824.0);
}

float wang_hash_noise(uint s)
{
  s = (s ^ 61u) ^ (s >> 16u);
  s *= 9u;
  s = s ^ (s >> 4u);
  s *= 0x27d4eb2du;
  s = s ^ (s >> 15u);

  return fract(float(s) / 4294967296.0);
}

float bi_mix( float v0, float v1, float v2, float v3, float x, float y ){
    
    float x1 = 1.0 - x;
    return ( 1.0 - y ) * ( v0 * x1 + v1 * x ) + y * ( v2 * x1 + v3 * x );
}

float tri_mix(float v0, float v1, float v2, float v3, float v4, float v5, float v6, float v7, float x, float y, float z ){

    float x1 = 1.0 - x;
    float y1 = 1.0 - y;
    float z1 = 1.0 - z;
    return z1 * ( y1 * ( v0 * x1 + v1 * x ) + y * ( v2 * x1 + v3 * x )) +
            z * ( y1 * ( v4 * x1 + v5 * x ) + y * ( v6 * x1 + v7 * x ));
}

float quad_mix(float v0,
               float v1,
               float v2,
               float v3,
               float v4,
               float v5,
               float v6,
               float v7,
               float v8,
               float v9,
               float v10,
               float v11,
               float v12,
               float v13,
               float v14,
               float v15,
               float x,
               float y,
               float z,
               float w){
  return mix( tri_mix( v0, v1, v2, v3, v4, v5, v6, v7, x, y, z ),
             tri_mix( v8, v9, v10, v11, v12, v13, v14, v15, x, y, z ),
             w );
}

float fade(float t)
{
  return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
}

float negate_if(float value, uint condition)
{
  return (condition != 0u) ? -value : value;
}

float noise_grad(uint hash, float x)
{
  uint h = hash & 15u;
  float g = 1u + (h & 7u);
  return negate_if(g, h & 8u) * x;
}

float noise_grad(uint hash, float x, float y)
{
  uint h = hash & 7u;
  float u = h < 4u ? x : y;
  float v = 2.0 * (h < 4u ? y : x);
  return negate_if(u, h & 1u) + negate_if(v, h & 2u);
}

float noise_grad(uint hash, float x, float y, float z)
{
  uint h = hash & 15u;
  float u = h < 8u ? x : y;
  float vt = ((h == 12u) || (h == 14u)) ? x : z;
  float v = h < 4u ? y : vt;
  return negate_if(u, h & 1u) + negate_if(v, h & 2u);
}

float noise_grad(uint hash, float x, float y, float z, float w)
{
  uint h = hash & 31u;
  float u = h < 24u ? x : y;
  float v = h < 16u ? y : z;
  float s = h < 8u ? z : w;
  return negate_if(u, h & 1u) + negate_if(v, h & 2u) + negate_if(s, h & 4u);
}

float noise_scale1(float result)
{
  return 0.2500 * result;
}

float noise_scale2(float result)
{
  return 0.6616 * result;
}

float noise_scale3(float result)
{
  return 0.9820 * result;
}

float noise_scale4(float result)
{
  return 0.8344 * result;
}

#define FLOORFRAC( x, x_int, x_fract ){ float x_floor = floor( x ); x_int = int( x_floor ); x_fract = x - x_floor; }

float noise_perlin1D( float x ){
    int X;
    float fx;

    FLOORFRAC( x, X, fx );

    float u = fade( fx );
    float r = mix( noise_grad( hash_int( X ), fx ), noise_grad( hash_int( X + 1 ), fx - 1.0 ), u );
    return r;
}

float noise_perlin2D( vec2 uv ){
  int X, Y;
  float fx, fy;

  FLOORFRAC( uv.x, X, fx );
  FLOORFRAC( uv.y, Y, fy );

  float u = fade( fx );
  float v = fade( fy );

  float r = bi_mix( noise_grad( hash_int2 (X, Y ), fx, fy ),
                   noise_grad( hash_int2( X + 1, Y ), fx - 1.0, fy ),
                   noise_grad( hash_int2( X, Y + 1 ), fx, fy - 1.0 ),
                   noise_grad( hash_int2( X + 1, Y + 1 ), fx - 1.0, fy - 1.0 ),
                   u,
                   v );

  return r;
}

float noise_perlin3D( vec3 vec ){
  int X, Y, Z;
  float fx, fy, fz;

  FLOORFRAC(vec.x, X, fx);
  FLOORFRAC(vec.y, Y, fy);
  FLOORFRAC(vec.z, Z, fz);

  float u = fade(fx);
  float v = fade(fy);
  float w = fade(fz);

  float r = tri_mix(noise_grad(hash_int3(X, Y, Z), fx, fy, fz),
                    noise_grad(hash_int3(X + 1, Y, Z), fx - 1, fy, fz),
                    noise_grad(hash_int3(X, Y + 1, Z), fx, fy - 1, fz),
                    noise_grad(hash_int3(X + 1, Y + 1, Z), fx - 1, fy - 1, fz),
                    noise_grad(hash_int3(X, Y, Z + 1), fx, fy, fz - 1),
                    noise_grad(hash_int3(X + 1, Y, Z + 1), fx - 1, fy, fz - 1),
                    noise_grad(hash_int3(X, Y + 1, Z + 1), fx, fy - 1, fz - 1),
                    noise_grad(hash_int3(X + 1, Y + 1, Z + 1), fx - 1, fy - 1, fz - 1),
                    u,
                    v,
                    w);

  return r;
}

float noise_perlin4D( vec4 vec ){
  int X, Y, Z, W;
  float fx, fy, fz, fw;

  FLOORFRAC(vec.x, X, fx);
  FLOORFRAC(vec.y, Y, fy);
  FLOORFRAC(vec.z, Z, fz);
  FLOORFRAC(vec.w, W, fw);

  float u = fade(fx);
  float v = fade(fy);
  float t = fade(fz);
  float s = fade(fw);

  float r = quad_mix(
      noise_grad(hash_int4(X, Y, Z, W), fx, fy, fz, fw),
      noise_grad(hash_int4(X + 1, Y, Z, W), fx - 1.0, fy, fz, fw),
      noise_grad(hash_int4(X, Y + 1, Z, W), fx, fy - 1.0, fz, fw),
      noise_grad(hash_int4(X + 1, Y + 1, Z, W), fx - 1.0, fy - 1.0, fz, fw),
      noise_grad(hash_int4(X, Y, Z + 1, W), fx, fy, fz - 1.0, fw),
      noise_grad(hash_int4(X + 1, Y, Z + 1, W), fx - 1.0, fy, fz - 1.0, fw),
      noise_grad(hash_int4(X, Y + 1, Z + 1, W), fx, fy - 1.0, fz - 1.0, fw),
      noise_grad(hash_int4(X + 1, Y + 1, Z + 1, W), fx - 1.0, fy - 1.0, fz - 1.0, fw),
      noise_grad(hash_int4(X, Y, Z, W + 1), fx, fy, fz, fw - 1.0),
      noise_grad(hash_int4(X + 1, Y, Z, W + 1), fx - 1.0, fy, fz, fw - 1.0),
      noise_grad(hash_int4(X, Y + 1, Z, W + 1), fx, fy - 1.0, fz, fw - 1.0),
      noise_grad(hash_int4(X + 1, Y + 1, Z, W + 1), fx - 1.0, fy - 1.0, fz, fw - 1.0),
      noise_grad(hash_int4(X, Y, Z + 1, W + 1), fx, fy, fz - 1.0, fw - 1.0),
      noise_grad(hash_int4(X + 1, Y, Z + 1, W + 1), fx - 1.0, fy, fz - 1.0, fw - 1.0),
      noise_grad(hash_int4(X, Y + 1, Z + 1, W + 1), fx, fy - 1.0, fz - 1.0, fw - 1.0),
      noise_grad(hash_int4(X + 1, Y + 1, Z + 1, W + 1), fx - 1.0, fy - 1.0, fz - 1.0, fw - 1.0),
      u,
      v,
      t,
      s);

  return r;
}

float snoise1D(float p)
{
  float r = noise_perlin1D(p);
  return (isinf(r)) ? 0.0 : noise_scale1(r);
}

float noise1D(float p)
{
  return 0.5 * snoise1D(p) + 0.5;
}

float snoise2D(vec2 p)
{
  float r = noise_perlin2D(p);
  return (isinf(r)) ? 0.0 : noise_scale2(r);
}

float noise2D(vec2 p)
{
  return 0.5 * snoise2D(p) + 0.5;
}

float snoise3D(vec3 p)
{
  float r = noise_perlin3D(p);
  return (isinf(r)) ? 0.0 : noise_scale3(r);
}

float noise3D(vec3 p)
{
  return 0.5 * snoise3D(p) + 0.5;
}

float snoise4D(vec4 p)
{
  float r = noise_perlin4D(p);
  return (isinf(r)) ? 0.0 : noise_scale4(r);
}

float noise4D(vec4 p)
{
  return 0.5 * snoise4D(p) + 0.5;
}

/* The fractal_noise functions are all exactly the same except for the input type. */
float fractal_noise1D(float p, float octaves, float roughness)
{
  float fscale = 1.0;
  float amp = 1.0;
  float maxamp = 0.0;
  float sum = 0.0;
  octaves = clamp(octaves, 0.0, 15.0);
  int n = int(octaves);
  for (int i = 0; i <= n; i++) {
    float t = noise1D(fscale * p);
    sum += t * amp;
    maxamp += amp;
    amp *= clamp(roughness, 0.0, 1.0);
    fscale *= 2.0;
  }
  float rmd = octaves - floor(octaves);
  if (rmd != 0.0) {
    float t = noise1D(fscale * p);
    float sum2 = sum + t * amp;
    sum /= maxamp;
    sum2 /= maxamp + amp;
    return (1.0 - rmd) * sum + rmd * sum2;
  }
  else {
    return sum / maxamp;
  }
}

/* The fractal_noise functions are all exactly the same except for the input type. */
float fractal_noise2D(vec2 p, float octaves, float roughness)
{
  float fscale = 1.0;
  float amp = 1.0;
  float maxamp = 0.0;
  float sum = 0.0;
  octaves = clamp(octaves, 0.0, 15.0);
  int n = int(octaves);
  for (int i = 0; i <= n; i++) {
    float t = noise2D(fscale * p);
    sum += t * amp;
    maxamp += amp;
    amp *= clamp(roughness, 0.0, 1.0);
    fscale *= 2.0;
  }
  float rmd = octaves - floor(octaves);
  if (rmd != 0.0) {
    float t = noise2D(fscale * p);
    float sum2 = sum + t * amp;
    sum /= maxamp;
    sum2 /= maxamp + amp;
    return (1.0 - rmd) * sum + rmd * sum2;
  }
  else {
    return sum / maxamp;
  }
}

/* The fractal_noise functions are all exactly the same except for the input type. */
float fractal_noise3D(vec3 p, float octaves, float roughness)
{
  float fscale = 1.0;
  float amp = 1.0;
  float maxamp = 0.0;
  float sum = 0.0;
  octaves = clamp(octaves, 0.0, 15.0);
  int n = int(octaves);
  for (int i = 0; i <= n; i++) {
    float t = noise3D(fscale * p);
    sum += t * amp;
    maxamp += amp;
    amp *= clamp(roughness, 0.0, 1.0);
    fscale *= 2.0;
  }
  float rmd = octaves - floor(octaves);
  if (rmd != 0.0) {
    float t = noise3D(fscale * p);
    float sum2 = sum + t * amp;
    sum /= maxamp;
    sum2 /= maxamp + amp;
    return (1.0 - rmd) * sum + rmd * sum2;
  }
  else {
    return sum / maxamp;
  }
}

/* The fractal_noise functions are all exactly the same except for the input type. */
float fractal_noise4D(vec4 p, float octaves, float roughness)
{
  float fscale = 1.0;
  float amp = 1.0;
  float maxamp = 0.0;
  float sum = 0.0;
  octaves = clamp(octaves, 0.0, 15.0);
  int n = int(octaves);
  for (int i = 0; i <= n; i++) {
    float t = noise4D(fscale * p);
    sum += t * amp;
    maxamp += amp;
    amp *= clamp(roughness, 0.0, 1.0);
    fscale *= 2.0;
  }
  float rmd = octaves - floor(octaves);
  if (rmd != 0.0) {
    float t = noise4D(fscale * p);
    float sum2 = sum + t * amp;
    sum /= maxamp;
    sum2 /= maxamp + amp;
    return (1.0 - rmd) * sum + rmd * sum2;
  }
  else {
    return sum / maxamp;
  }
}

float random_float_offset(float seed){
    return 100.0 + hash_float_to_float(seed) * 100.0;
}

vec2 random_vec2_offset(float seed){
    return vec2(
      100.0 + hash_vec2_to_float(vec2(seed, 0.0)) * 100.0,
      100.0 + hash_vec2_to_float(vec2(seed, 1.0)) * 100.0);
}

vec3 random_vec3_offset(float seed){
  return vec3(
    100.0 + hash_vec2_to_float(vec2(seed, 0.0)) * 100.0,
    100.0 + hash_vec2_to_float(vec2(seed, 1.0)) * 100.0,
    100.0 + hash_vec2_to_float(vec2(seed, 2.0)) * 100.0);
}

vec4 random_vec4_offset(float seed){
  return vec4(
    100.0 + hash_vec2_to_float(vec2(seed, 0.0)) * 100.0,
    100.0 + hash_vec2_to_float(vec2(seed, 1.0)) * 100.0,
    100.0 + hash_vec2_to_float(vec2(seed, 2.0)) * 100.0,
    100.0 + hash_vec2_to_float(vec2(seed, 3.0)) * 100.0);
}

// VORONOI

float voronoi_distance1D(float a, float b, float metric, float exponent){
  return distance(a, b);
}

float voronoi_distance2D(vec2 a, vec2 b, float metric, float exponent){
  if (metric == 0.0)  // SHD_VORONOI_EUCLIDEAN
  {
    return distance(a, b);
  }
  else if (metric == 1.0)  // SHD_VORONOI_MANHATTAN
  {
    return abs(a.x - b.x) + abs(a.y - b.y);
  }
  else if (metric == 2.0)  // SHD_VORONOI_CHEBYCHEV
  {
    return max(abs(a.x - b.x), abs(a.y - b.y));
  }
  else if (metric == 3.0)  // SHD_VORONOI_MINKOWSKI
  {
    return pow(pow(abs(a.x - b.x), exponent) + pow(abs(a.y - b.y), exponent), 1.0 / exponent);
  }
  else {
    return 0.0;
  }
}

float voronoi_distance(vec3 a, vec3 b, float metric, float exponent)
{
  if (metric == 0.0)  // SHD_VORONOI_EUCLIDEAN
  {
    return distance(a, b);
  }
  else if (metric == 1.0)  // SHD_VORONOI_MANHATTAN
  {
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z);
  }
  else if (metric == 2.0)  // SHD_VORONOI_CHEBYCHEV
  {
    return max(abs(a.x - b.x), max(abs(a.y - b.y), abs(a.z - b.z)));
  }
  else if (metric == 3.0)  // SHD_VORONOI_MINKOWSKI
  {
    return pow(pow(abs(a.x - b.x), exponent) + pow(abs(a.y - b.y), exponent) +
                   pow(abs(a.z - b.z), exponent),
               1.0 / exponent);
  }
  else {
    return 0.0;
  }
}

float voronoi_distance(vec4 a, vec4 b, float metric, float exponent)
{
  if (metric == 0.0)  // SHD_VORONOI_EUCLIDEAN
  {
    return distance(a, b);
  }
  else if (metric == 1.0)  // SHD_VORONOI_MANHATTAN
  {
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z) + abs(a.w - b.w);
  }
  else if (metric == 2.0)  // SHD_VORONOI_CHEBYCHEV
  {
    return max(abs(a.x - b.x), max(abs(a.y - b.y), max(abs(a.z - b.z), abs(a.w - b.w))));
  }
  else if (metric == 3.0)  // SHD_VORONOI_MINKOWSKI
  {
    return pow(pow(abs(a.x - b.x), exponent) + pow(abs(a.y - b.y), exponent) +
                   pow(abs(a.z - b.z), exponent) + pow(abs(a.w - b.w), exponent),
               1.0 / exponent);
  }
  else {
    return 0.0;
  }
}

#endif