from pipeline_node import *

SKY_SHADER = None

SKY_SOURCE = generate_source('''

#include "Node Utils/common.glsl"
#include "Common/Color.glsl"
#include "Common/Transform.glsl"

#include "MixRGB.internal.glsl"

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
''')

class EssentialsSky( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Clouds' : ( 'sampler2D', '' ),
            'Lower Sky' : ( 'vec4', ( 0.67, 0.85, 1.0, 1.0 )),
            'Upper Sky' : ( 'vec4', ( 0.21, 0.3, 0.54, 1.0 )),
            'Exponent' : ( 'float', 0.75 ),
            'Cloud Occlusion' : ( 'float', 0.5 ),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Occlusion' : ( 'sampler2D', '' ),
        }
    def get_texture_targets( self, resolution:tuple[int,int]) -> list[TextureTarget]:
        return [ 
            TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution ), 
            TextureTarget( 'OCCLUSION', TextureFormat.RGBA16F, resolution )]
    
    def get_render_targets(self, resolution: tuple[int, int], inputs) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ 
                TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution ),
                TextureTarget( 'OCCLUSION', TextureFormat.RGBA16F, resolution )]
        }
    
    def render( self, inputs: dict, outputs: dict ):
        
        global SKY_SHADER
        if not SKY_SHADER:
            SKY_SHADER = self.compile_shader( SKY_SOURCE, include_paths = [get_shader_functions_path( )])
        
        self.render_shader( SKY_SHADER, self.get_render_target( 'MAIN' ),
            textures = {
                'color_texture' : inputs[ 'Color' ],
                'cloud_texture' : inputs[ 'Clouds' ]
            },
            uniforms = {
                'lower_sky' : inputs[ 'Lower Sky' ],
                'upper_sky' : inputs[ 'Upper Sky' ],
                'exponent' : inputs[ 'Exponent' ],
                'cloud_occlusion_factor' : inputs[ 'Cloud Occlusion' ],
            }
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )
        outputs[ 'Occlusion' ]  = self.get_output( 'MAIN', 'OCCLUSION' )

NODE = EssentialsSky