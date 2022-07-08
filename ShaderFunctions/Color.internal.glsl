#ifndef SHADINGESSENTIALS_COLOR_GLSL
#define SHADINGESSENTIALS_COLOR_GLSL

#include "Common/Color.glsl"

void hue_saturation_value( float h, float s, float v, float fac, bool invert, vec4 color, out vec4 result ){
    vec3 hsv = rgb_to_hsv( color.rgb );
    hsv.x = fract( hsv.x + h + 0.5 );
    hsv.y = clamp( hsv.y * s, 0.0, 1.0 );
    hsv.z *= v;
    result = vec4( hsv_to_rgb( hsv ), color.a );
    result = mix( color, result, abs( float( invert ) - fac ));
}

vec4 brightness_contrast( vec4 col, float brightness, float contrast ){
    float a = 1.0 + contrast;
    float b = brightness - contrast * 0.5;
    vec4 result;
    result.r = max( a * col.r + b, 0.0 );
    result.g = max( a * col.g + b, 0.0 );
    result.b = max( a * col.b + b, 0.0 );
    result.a = col.a;
    return result;
}

vec4 gamma_correction( vec4 col, float gamma ){
    vec4 result = col;

    if( col.r > 0.0 ){
        result.r = pow( col.r, gamma );
    }
    if( col.g > 0.0 ){
        result.g = pow( col.g, gamma );
    }
    if( col.b > 0.0 ){
        result.b = pow( col.b, gamma );
    }
    return result;
}

vec4 color_invert( vec4 col, float fac ){
    vec4 result;
    result.r = 1 - col.r;
    result.g = 1 - col.g;
    result.b = 1 - col.b;
    result.a = col.a;
    return mix( col, result, fac );
}

vec4 color_paletting( vec4 col, vec4 palette[16] ){

    // vec4 palette[4] = vec4[]( vec4( 1.0, 0.0, 0.0, 1.0 ), vec4( 0.0, 1.0, 0.0, 1.0 ), vec4( 0.0, 0.0, 1.0, 1.0 ), vec4( 0.0, 0.0, 0.0, 1.0 ));
    vec4 result = vec4( 0.0, 0.0, 0.0, 1.0 );
    float min_dist = 8.0;
    for( int i; i < 16; i++ ){
        vec4 palette_color = palette[i];
        float dist = distance( col, palette_color );
        if( dist < min_dist ){
            result = palette_color;
            min_dist = min( dist, min_dist );
        }
    }
    return result;
}

#endif
