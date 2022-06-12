
#ifdef PIXEL_SHADER
#include "NPR_ScreenShader.glsl"
#include "Node Utils/node_utils.glsl"
// OUT_SCREEN_SHADER_COLOR
layout( location = 0 ) out vec4 OUT_RESULT;
uniform sampler2D color_texture;
uniform float bloom_radius;
uniform int samples;
uniform float bloom_exponent;
uniform float bloom_intensity;

void SCREEN_SHADER(){

    PIXEL_SETUP_INPUT();

    // vec2 uv = screen_uv( );
    // vec4 screen_color = sampler2D_sample( color_texture, uv );

    // float blur_radius = render_resolution( ).y * bloom_radius;
    // vec3 blurred_color = jitter_blur( color_texture, uv, blur_radius, 5.0, samples ).xyz;
    // blurred_color.r = pow( blurred_color.r, bloom_exponent ) * bloom_intensity;
    // blurred_color.g = pow( blurred_color.g, bloom_exponent ) * bloom_intensity;
    // blurred_color.b = pow( blurred_color.b, bloom_exponent ) * bloom_intensity;
    // screen_color.xyz += blurred_color;
    // OUT_SCREEN_SHADER_COLOR = screen_color;
    OUT_RESULT = vec4(1.0, 0.0, 0.0, 1.0 );
}
#endif //PIXEL_SHADER