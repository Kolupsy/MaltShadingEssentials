
#include "Common.glsl"
#include "Filters/Blur.glsl"
#include "Node Utils/common.glsl"
#include "../ShaderFunctions/Utils.internal.glsl"

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

uniform sampler2D color_texture;

uniform vec3 bloom_settings; // x = bloom exponent y = bloom intensity z = bloom radius
uniform int samples;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];
    float bloom_exponent = bloom_settings.x;
    float bloom_intensity = bloom_settings.y;
    float bloom_radius = bloom_settings.z;
    vec4 screen_color = texture( color_texture, uv );
    vec3 blurred_color = jitter_blur( color_texture, uv, render_size( ) * bloom_radius, 5.0, samples ).xyz;
    

    blurred_color.r = pow( blurred_color.r, bloom_exponent ) * bloom_intensity;
    blurred_color.g = pow( blurred_color.g, bloom_exponent ) * bloom_intensity;
    blurred_color.b = pow( blurred_color.b, bloom_exponent ) * bloom_intensity;
    screen_color.xyz += blurred_color;
    
    RESULT = screen_color;
}

#endif