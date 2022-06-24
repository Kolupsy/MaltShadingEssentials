#include "Common.glsl"
#include "Node Utils/common.glsl"
#include "Common/Color.glsl"
#include "Common/Transform.glsl"

#include "../ShaderFunctions/MixRGB.internal.glsl"

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

uniform sampler2D color_texture;
uniform sampler2D cloud_texture;

uniform vec4 lower_sky;
uniform vec4 upper_sky;
uniform float exponent;
uniform float cloud_occlusion_factor;

layout (location = 0) out vec4 OUT_COLOR;
layout (location = 1) out vec4 OUT_OCCLUSION;

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 uv = UV[0];
    vec3 world_coords = view_direction( );

    vec4 foreground = texture( color_texture, uv );
    vec4 cloud_mask = texture( cloud_texture, uv );

    float grad = clamp( pow( world_coords.z, exponent ), 0.0, 1.0 );
    vec4 sky_gradient = mix( lower_sky, upper_sky, grad );
    vec4 full_sky;
    mix_soft_light( 1.0, sky_gradient, cloud_mask, full_sky );
    
    OUT_COLOR = alpha_blend( full_sky, foreground );
    OUT_OCCLUSION = vec4( 0.0, 0.0, 0.0, max( foreground.a, cloud_mask.x * cloud_occlusion_factor ));
}

#endif