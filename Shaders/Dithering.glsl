#include "Common.glsl"
#include "Filters/Blur.glsl"
#include "Node Utils/common.glsl"
#include "../ShaderFunctions/Color.internal.glsl"

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

uniform sampler2D color_texture;
uniform sampler2D threshold_texture;
uniform float gamma;
uniform vec4 darker_color;
uniform vec4 lighter_color;

layout (location = 0) out vec4 OUT_COLOR;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];
    vec4 color = texture( color_texture, uv );
    color = gamma_correction( color, gamma );
    float gradient = ( color.x + color.y + color.z ) / 3.0;
    
    vec2 noise_uv = uv * ( render_resolution( ) / vec2( textureSize( threshold_texture, 0 ) ));
    float threshold = texture(  threshold_texture, noise_uv ).x;

    OUT_COLOR = mix( darker_color, lighter_color, ( gradient > threshold ) ? 1.0 : 0.0 );
}

#endif