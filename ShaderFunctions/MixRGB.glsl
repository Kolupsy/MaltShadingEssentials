#ifndef SHADINGESSENTIALS_MIXRGB_GLSL
#define SHADINGESSENTIALS_MIXRGB_GLSL
/* META @meta: internal=true; */
void mix_blend(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result = mix(col1, col2, fac);
  result.a = col1.a;
}

/* META @meta: internal=true; */
void mix_add(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result = mix(col1, col1 + col2, fac);
  result.a = col1.a;
}

/* META @meta: internal=true; */
void mix_multiply(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result = mix(col1, col1 * col2, fac);
  result.a = col1.a;
}

/* META @meta: internal=true; */
void mix_subtract(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result = mix(col1, col1 - col2, fac);
  result.a = col1.a;
}

/* META @meta: internal=true; */
void mix_screen(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float facm = 1.0 - fac;

  result = vec4(1.0) - (vec4(facm) + fac * (vec4(1.0) - col2)) * (vec4(1.0) - col1);
  result.a = col1.a;
}

/* META @meta: internal=true; */
void mix_divide(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float facm = 1.0 - fac;

  result = col1;

  if (col2.r != 0.0) {
    result.r = facm * result.r + fac * result.r / col2.r;
  }
  if (col2.g != 0.0) {
    result.g = facm * result.g + fac * result.g / col2.g;
  }
  if (col2.b != 0.0) {
    result.b = facm * result.b + fac * result.b / col2.b;
  }
}

/* META @meta: internal=true; */
void mix_difference(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result = mix(col1, abs(col1 - col2), fac);
  result.a = col1.a;
}

/* META @meta: internal=true; */
void mix_darken(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result.rgb = mix(col1.rgb, min(col1.rgb, col2.rgb), fac);
  result.a = col1.a;
}

/* META @meta: internal=true; */
void mix_lighten(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result.rgb = mix(col1.rgb, max(col1.rgb, col2.rgb), fac);
  result.a = col1.a;
}

/* META @meta: internal=true; */
void mix_overlay(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float facm = 1.0 - fac;

  result = col1;

  if (result.r < 0.5) {
    result.r *= facm + 2.0 * fac * col2.r;
  }
  else {
    result.r = 1.0 - (facm + 2.0 * fac * (1.0 - col2.r)) * (1.0 - result.r);
  }

  if (result.g < 0.5) {
    result.g *= facm + 2.0 * fac * col2.g;
  }
  else {
    result.g = 1.0 - (facm + 2.0 * fac * (1.0 - col2.g)) * (1.0 - result.g);
  }

  if (result.b < 0.5) {
    result.b *= facm + 2.0 * fac * col2.b;
  }
  else {
    result.b = 1.0 - (facm + 2.0 * fac * (1.0 - col2.b)) * (1.0 - result.b);
  }
}

/* META @meta: internal=true; */
void mix_dodge(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result = col1;

  if (result.r != 0.0) {
    float tmp = 1.0 - fac * col2.r;
    if (tmp <= 0.0) {
      result.r = 1.0;
    }
    else if ((tmp = result.r / tmp) > 1.0) {
      result.r = 1.0;
    }
    else {
      result.r = tmp;
    }
  }
  if (result.g != 0.0) {
    float tmp = 1.0 - fac * col2.g;
    if (tmp <= 0.0) {
      result.g = 1.0;
    }
    else if ((tmp = result.g / tmp) > 1.0) {
      result.g = 1.0;
    }
    else {
      result.g = tmp;
    }
  }
  if (result.b != 0.0) {
    float tmp = 1.0 - fac * col2.b;
    if (tmp <= 0.0) {
      result.b = 1.0;
    }
    else if ((tmp = result.b / tmp) > 1.0) {
      result.b = 1.0;
    }
    else {
      result.b = tmp;
    }
  }
}

/* META @meta: internal=true; */
void mix_burn(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float tmp, facm = 1.0 - fac;

  result = col1;

  tmp = facm + fac * col2.r;
  if (tmp <= 0.0) {
    result.r = 0.0;
  }
  else if ((tmp = (1.0 - (1.0 - result.r) / tmp)) < 0.0) {
    result.r = 0.0;
  }
  else if (tmp > 1.0) {
    result.r = 1.0;
  }
  else {
    result.r = tmp;
  }

  tmp = facm + fac * col2.g;
  if (tmp <= 0.0) {
    result.g = 0.0;
  }
  else if ((tmp = (1.0 - (1.0 - result.g) / tmp)) < 0.0) {
    result.g = 0.0;
  }
  else if (tmp > 1.0) {
    result.g = 1.0;
  }
  else {
    result.g = tmp;
  }

  tmp = facm + fac * col2.b;
  if (tmp <= 0.0) {
    result.b = 0.0;
  }
  else if ((tmp = (1.0 - (1.0 - result.b) / tmp)) < 0.0) {
    result.b = 0.0;
  }
  else if (tmp > 1.0) {
    result.b = 1.0;
  }
  else {
    result.b = tmp;
  }
}

/* META @meta: internal=true; */
void mix_hue(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float facm = 1.0 - fac;

  result = col1;

  vec4 hsv, hsv2, tmp;
  hsv2.rgb = rgb_to_hsv(col2.rgb);

  if (hsv2.y != 0.0) {
    hsv.rgb = rgb_to_hsv(result.rgb);
    hsv.x = hsv2.x;
    tmp.rgb = hsv_to_rgb(hsv.rgb);

    result = mix(result, tmp, fac);
    result.a = col1.a;
  }
}

/* META @meta: internal=true; */
void mix_saturation(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float facm = 1.0 - fac;

  result = col1;

  vec4 hsv, hsv2;
  hsv.rgb = rgb_to_hsv(result.rgb);

  if (hsv.y != 0.0) {
    hsv2.rgb = rgb_to_hsv(col2.rgb);

    hsv.y = facm * hsv.y + fac * hsv2.y;
    result.rgb = hsv_to_rgb(hsv.rgb);
  }
}

/* META @meta: internal=true; */
void mix_value(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float facm = 1.0 - fac;

  vec4 hsv, hsv2;
  hsv.rgb = rgb_to_hsv(col1.rgb);
  hsv2.rgb = rgb_to_hsv(col2.rgb);

  hsv.z = facm * hsv.z + fac * hsv2.z;
  result.rgb = hsv_to_rgb(hsv.rgb);
}

/* META @meta: internal=true; */
void mix_color(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float facm = 1.0 - fac;

  result = col1;

  vec4 hsv, hsv2, tmp;
  hsv2.rgb = rgb_to_hsv(col2.rgb);

  if (hsv2.y != 0.0) {
    hsv.rgb = rgb_to_hsv(result.rgb);
    hsv.x = hsv2.x;
    hsv.y = hsv2.y;
    tmp.rgb = hsv_to_rgb(hsv.rgb);

    result = mix(result, tmp, fac);
    result.a = col1.a;
  }
}

/* META @meta: internal=true; */
void mix_soft_light(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  float facm = 1.0 - fac;

  vec4 one = vec4(1.0);
  vec4 scr = one - (one - col2) * (one - col1);
  result = facm * col1 + fac * ((one - col1) * col2 * col1 + col1 * scr);
}

/* META @meta: internal=true; */
void mix_linear_light(float fac, vec4 col1, vec4 col2, out vec4 result)
{
  fac = clamp(fac, 0.0, 1.0);
  result = col1 + fac * (2.0 * (col2 - vec4(0.5)));
}

/* META @meta: internal=true; */
void mix_clamp_color(vec3 vec, vec3 min, vec3 max, out vec3 out_vec)
{
  out_vec = clamp(vec, min, max);
}

#endif
