import pathlib
from pipeline_node import *

_SHADER = None

SHADERPATH = str( pathlib.Path( __file__ ).parent.parent.joinpath( 'Shaders', 'SunFlare.glsl' ))

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
        
        global _SHADER
        if not _SHADER:
            _SHADER = self.compile_shader( f'#include "{SHADERPATH}"' )

        self.setup_lights_buffer( _SHADER, inputs[ 'Scene' ])
        
        self.render_shader( _SHADER, self.get_render_target( 'MAIN' ),
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