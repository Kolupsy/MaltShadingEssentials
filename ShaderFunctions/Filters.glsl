#ifndef SHADINGESSENTIALS_FILTER_GLSL
#define SHADINGESSENTIALS_FILTER_GLSL

vec4 sharpen( sampler2D tex, vec2 uv, float sharpness ){

    vec4 base = texture( tex, uv );
    if( sharpness <= 0.0 ){
        return base;
    }

    vec2 res = render_resolution( );
    vec3 neighbors;

    vec2 offsets[4] = vec2[]( vec2( 0, 1 ), vec2( 0, -1 ), vec2( 1, 0 ), vec2( -1, 0 ));
    for( int i = 0; i < 4; ++i ){
        neighbors += texture( tex, uv + offsets[ i ] / res ).rgb * vec3( - sharpness );
    }
    base.rgb += ( base.rgb * vec3( sharpness * 4 )) + neighbors;
    return base;
}

#endif //SHADINGESSENTIALS_FILTER_GLSL