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

float uv_overflow( vec2 uv ){
    uv = abs( uv - vec2( 0.5 ));
    float result = max( uv.x, uv.y );
    result = result * 2.0 - 1.0;
    return result;
}

vec3 ray_hit( vec3 incoming, vec3 position, float pos_component, float incoming_component, float dist ){
    float t = ( dist - pos_component ) / incoming_component;
    return ( incoming * vec3( t )) + position;
}

vec2 curve_view_uv( vec3 tangent, vec3 incoming, vec3 normal, vec2 uv ){

    vec3 screen_binormal = transform_normal( CAMERA, cross( tangent, incoming ));
    vec3 screen_normal = transform_normal( CAMERA, normal );
    float y_grad = dot( screen_binormal, screen_normal );
    return vec2( uv.x, ( y_grad + 1.0 ) * 0.5 );
}

#endif //SHADINGESSENTIALS_UTILS_GLSL
