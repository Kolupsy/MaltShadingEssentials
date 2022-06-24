#include "Node Utils/common.glsl"

#ifndef SHADINGESSENTIALS_UTILS_GLSL
#define SHADINGESSENTIALS_UTILS_GLSL

float render_size( ){
    vec2 res = render_resolution( );
    return ( res.x + res.y ) * 0.5;
}

float get_texture_size( sampler2D tex ){
    ivec2 res = textureSize( tex, 0 );
    return float( res.x + res.y ) * 0.5;
}

vec2 aspect_ratio( ){
    vec2 res = render_resolution( );
    return vec2( res.x / res.y, 1.0 );
}

#endif //SHADINGESSENTIALS_UTILS_GLSL
