from pipeline_node import *

LF_SHADER = None

class EssentialsLensFlare( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Depth' : ( 'sampler2D', '' ),
            'Scene' : ( 'OTHER', 'Scene' ),
            'Sun Factor' : ( 'float', 1.0 ),
            'Point Factor' : ( 'float', 1.0 ),
            'Spot Factor' : ( 'float', 1.0 ),
            'Edge Fade' : ( 'float', 5.0 ),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' )
        }

    def get_render_targets( self, resolution: tuple[int, int]) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )]
        }
    
    
    def render( self, inputs: dict, outputs: dict ):
        
        global LF_SHADER
        if not LF_SHADER:
            LF_SHADER = self.compile_shader( get_shader_source( 'LensFlare.glsl' ))

        self.setup_lights_buffer( LF_SHADER, inputs[ 'Scene' ])
        
        self.render_shader( LF_SHADER, self.get_render_target( 'MAIN' ),
            textures = {
                'color_texture' : inputs[ 'Color' ],
                'depth_texture' : inputs[ 'Depth' ]
            },
            uniforms = {
                'light_factors' : ( inputs[ 'Sun Factor' ], inputs[ 'Point Factor' ], inputs[ 'Spot Factor' ]),
                'edge_fade' : inputs[ 'Edge Fade' ],
            }
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsLensFlare