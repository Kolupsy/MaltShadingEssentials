from pipeline_node import *

VIGNETTE_SHADER = None
VIGNETTE_SOURCE = generate_source('''

uniform sampler2D color_texture;
uniform vec4 vignette_color = vec4( 0.0, 0.0, 0.0, 1.0 );
uniform float radius = 1.0;
uniform float smoothness = 0.3;
uniform int type = 0;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 uv = UV[0];
    vec2 c = ( uv - 0.5 ) * 2;
    vec2 s = vec2( textureSize( color_texture, 0 ));
    vec2 aspect = vec2( s.x / s.y, 1.0 );

    vec4 original = texture( color_texture, uv );

    float l;

    switch( type ){
        case 0:
            l = length( c ); break;
        case 1:
            l = length( c * aspect ); break;
        case 2:
            c = abs( c );
            max( c.x, c.y );
            break;
    }

    float gradient = smoothstep( radius - smoothness, radius + smoothness, l );

    RESULT = mix( original, vignette_color, clamp( gradient, 0.0, 1.0 ));
}
''')

class EssentialsVignette( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Vignette' : ( 'vec4', ( 0.0, 0.0, 0.0, 1.0 )),
            'Radius' : ( 'float', 1.0 ),
            'Smoothness' : ( 'float', 0.1 ),
            'Type' : ( 'int', 0 )
        }
    
    @classmethod
    def static_outputs(cls) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
        }
    
    def get_render_targets( self, resolution: tuple[int, int], inputs) -> dict[str, list[TextureTarget]]:
        return{
            'VIGNETTE' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, resolution )]
        }
    
    def render( self, inputs: dict, outputs: dict ) -> None:
        
        global VIGNETTE_SHADER
        if not VIGNETTE_SHADER:
            VIGNETTE_SHADER = self.compile_shader( VIGNETTE_SOURCE, include_paths = [ get_shader_functions_path( )] )
        
        self.render_shader( VIGNETTE_SHADER, self.get_render_target( 'VIGNETTE' ),
            textures = { 'color_texture' : inputs[ 'Color' ]},
            uniforms = {
                'vignette_color' : inputs[ 'Vignette' ],
                'radius' : inputs[ 'Radius' ],
                'smoothness' : inputs[ 'Smoothness' ],
                'type' : inputs[ 'Type' ],
            }
        )

        outputs[ 'Color' ] = self.get_output( 'VIGNETTE', 'Main' )

NODE = EssentialsVignette