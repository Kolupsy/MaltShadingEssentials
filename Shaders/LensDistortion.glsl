#include "Common.glsl"
#include "Filters/Blur.glsl"
#include "Node Utils/common.glsl"
#include "../ShaderFunctions/Utils.internal.glsl"

// https://www.shadertoy.com/view/4lSGRw
vec2 compute_distored_UVs( vec2 uv, float k, float kcube ){
    
    vec2 t = uv - .5;
    float r2 = t.x * t.x + t.y * t.y;
	float f = 0.;
    
    if( kcube == 0.0 ){
        f = 1. + r2 * k;
    }else{
        f = 1. + r2 * ( k + kcube * sqrt( r2 ) );
    }
    return f * t + .5;
}

vec4 distorted_channel( sampler2D tex, vec2 uv, float k, float kcube, float offset, float blur, int channel ){
    float offset_k = k;
    if( channel == 0){
        offset_k = k + offset;
    }
    if( channel == 2){
        offset_k = k - offset;
    }

    vec2 nUv = compute_distored_UVs( uv, offset_k, kcube );
    
    if( abs( blur ) < 1.0 ){
        return texture( tex, nUv );
    }else{
        vec2 dUv = nUv - uv;
        float diff = dUv.x * dUv.x + dUv.y * dUv.y;
        diff = min( diff * blur, 3000 );
        return box_blur( tex, nUv, diff, false );
    }
}

vec4 distorted_image( sampler2D tex, vec2 uv, float distortion, float offset, float blur ){

    float k = 1.0 * distortion * 0.9;
    float kcube = 0.5 * distortion;
    offset = offset * distortion * 0.5;
    float red = distorted_channel( tex, uv, k, kcube, offset, blur, 0 ).r;
    float green = distorted_channel( tex, uv, k, kcube, offset, blur, 1 ).g;
    float blue = distorted_channel( tex, uv, k, kcube, offset, blur, 2 ).b;
    return vec4( red, green, blue, 1.0 );
}

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

uniform sampler2D color_texture;

uniform float distortion;
uniform float offset;
uniform float blur;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];
    RESULT = distorted_image( color_texture, uv, distortion, offset, render_size( ) * blur );
}

#endif