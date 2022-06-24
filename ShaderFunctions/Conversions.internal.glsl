#ifndef SHADINGESSENTIALS_CONVERSIONS_GLSL
#define SHADINGESSENTIALS_CONVERSIONS_GLSL

// CONVERSIONS

// FROM VEC2
float float_from_vec2( vec2 uv ){
    return ( uv.x + uv.y )/2;
}
int int_from_vec2( vec2 uv ){
    return int( float_from_vec2( uv ));
}

// FROM VEC3
float float_from_vec3( vec3 col ){
    return ( col.x + col.y + col.z ) / 3;
}
int int_from_vec3( vec3 col ){
    return int( float_from_vec3( col ));
}

// FROM VEC4
float float_from_vec4( vec4 col ){
    return float_from_vec3( col.xyz ) * col.w;
}
int int_from_vec4( vec4 col ){
    return int( float_from_vec4( col ));
}

// OTHER
vec4 vec4_from_float_2( float f ){
    return vec4( f, f, f, 1 );
}
#endif
