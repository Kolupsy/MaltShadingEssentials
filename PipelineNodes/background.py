from pipeline_node import *

SHADER = None

BACKGROUND_SOURCE = generate_source('''
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
''')

class EssentialsBackground( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Background' : ( 'vec4', ( 0.1, 0.1, 0.1, 1.0 ))
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
        }
    
    def get_render_targets(self, resolution: tuple[int, int], inputs) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )]
        }
    
    def render( self, inputs: dict, outputs: dict ):
        
        global SHADER
        if not SHADER:
            SHADER = self.compile_shader( BACKGROUND_SOURCE )
        
        self.render_shader( SHADER, self.get_render_target( 'MAIN' ),
            textures = { 'color_texture' : inputs[ 'Color' ]},
            uniforms = { 'background_color' : inputs[ 'Background' ]}
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsBackground