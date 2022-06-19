#include "Common.glsl"
#include "Filters/Blur.glsl"
#include "Node Utils/common.glsl"
#include "Common/Color.glsl"

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

uniform sampler2D color_texture;
uniform vec4 background_color;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 uv = UV[0];
    vec4 col = texture( color_texture, uv );
    col = alpha_blend( background_color, col );
    
    RESULT = col;
}

#endif