from pipeline_node import *

SF_SHADER = None

class EssentialsSunFlare( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Occlusion' : ( 'sampler2D', '' ),
            'Scene' : ( 'OTHER', 'Scene' ),
            'Intensity' : ( 'float', 1.0 ),
            'Edge Fade' : ( 'float', 5.0 ),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' )
        }
    
    def get_render_targets(self, resolution: tuple[int, int]) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )]
        }
    
    def render( self, inputs: dict, outputs: dict ):
        
        global SF_SHADER
        if not SF_SHADER:
            SF_SHADER = self.compile_shader( get_shader_source( 'SunFlare.glsl' ), include_paths = [get_shader_functions_path( )])

        self.setup_lights_buffer( SF_SHADER, inputs[ 'Scene' ])
        
        self.render_shader( SF_SHADER, self.get_render_target( 'MAIN' ),
            textures = {
                'color_texture' : inputs[ 'Color' ],
                'occlusion_texture' : inputs[ 'Occlusion' ]
            },
            uniforms = {
                'intensity_factor' : inputs[ 'Intensity' ],
                'edge_fade' : inputs[ 'Edge Fade' ],
            }
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsSunFlare