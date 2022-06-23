#include "Node Utils/common.glsl"

float render_size( ){
    vec2 res = render_resolution( );
    return ( res.x + res.y ) * 0.5;
}

float get_texture_size( sampler2D tex ){
    ivec2 res = textureSize( tex, 0 );
    return float( res.x + res.y ) * 0.5;
}