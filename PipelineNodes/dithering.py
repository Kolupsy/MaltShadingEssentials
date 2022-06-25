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
    def get_texture_targets( self ) -> list[str]:
        return [ 'COLOR' ]
    
    def render( self, inputs: dict, outputs: dict ):
        
        global _SHADER
        if not _SHADER:
            _SHADER = self.compile_shader( f'#include "{SHADERPATH}"' )
        
        self.render_shader( _SHADER,
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
        outputs[ 'Color' ] = self.texture_targets[ 'COLOR' ]

NODE = EssentialsDithering