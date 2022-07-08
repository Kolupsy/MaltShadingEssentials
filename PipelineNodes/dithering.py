import pathlib
from pipeline_node import *

_SHADER = None

SHADERPATH = str( pathlib.Path( __file__ ).parent.parent.joinpath( 'Shaders', 'Dithering.glsl' ))

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
    
    def get_render_targets( self, resolution: tuple[int, int]) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )]
        }
    

    def render( self, inputs: dict, outputs: dict ):
        
        global _SHADER
        if not _SHADER:
            _SHADER = self.compile_shader( f'#include "{SHADERPATH}"' )
        
        self.render_shader( _SHADER, self.get_render_target( 'MAIN' ),
            textures = {
                'color_texture' : inputs[ 'Color' ],
                'threshold_texture' : inputs[ 'Noise' ],
            },
            uniforms = {
                'gamma' : inputs[ 'Gamma' ],
                'darker_color' : inputs[ 'Darker' ],
                'lighter_color' : inputs[ 'Lighter' ],
            }
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsDithering