from pipeline_node import *

DITHER_SHADER = None

DITHER_SOURCE = generate_source('''

#include "Filters/Blur.glsl"
#include "Node Utils/common.glsl"
#include "Common/Color.glsl"

uniform sampler2D color_texture;
uniform sampler2D threshold_texture;
uniform float gamma_value;
uniform vec4 darker_color;
uniform vec4 lighter_color;

layout (location = 0) out vec4 OUT_COLOR;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];
    vec4 color = texture( color_texture, uv );
    color = gamma( color, gamma_value );
    float gradient = ( color.x + color.y + color.z ) / 3.0;
    
    vec2 noise_uv = uv * ( render_resolution( ) / vec2( textureSize( threshold_texture, 0 ) ));
    float threshold = texture(  threshold_texture, noise_uv ).x;

    OUT_COLOR = mix( darker_color, lighter_color, ( gradient > threshold ) ? 1.0 : 0.0 );
}
''')

class EssentialsDithering( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Noise' : ( 'sampler2D', '' ),
            'Gamma' : ( 'float', 1.0 ),
            'Darker' : ( 'vec4', ( 0.06, 0.1, 0.05, 1.0 )),
            'Lighter' : ( 'vec4', ( 1.0, 0.97, 0.7, 1.0 )),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' )
        }
    
    def get_render_targets( self, resolution: tuple[int, int], inputs) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )]
        }
    

    def render( self, inputs: dict, outputs: dict ):
        
        global DITHER_SHADER
        if not DITHER_SHADER:
            DITHER_SHADER = self.compile_shader( DITHER_SOURCE, include_paths = [get_shader_functions_path( )])
        
        self.render_shader( DITHER_SHADER, self.get_render_target( 'MAIN' ),
            textures = {
                'color_texture' : inputs[ 'Color' ],
                'threshold_texture' : inputs[ 'Noise' ],
            },
            uniforms = {
                'gamma_value' : inputs[ 'Gamma' ],
                'darker_color' : inputs[ 'Darker' ],
                'lighter_color' : inputs[ 'Lighter' ],
            }
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsDithering