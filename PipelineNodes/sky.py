import pathlib
from pipeline_node import *

_SHADER = None

SHADERPATH = str( pathlib.Path( __file__ ).parent.parent.joinpath( 'Shaders', 'Skybox.glsl' ))

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
    def get_texture_targets( self ) -> list[str]:
        return [ 'COLOR', 'OCCLUSION' ]
    
    def render( self, inputs: dict, outputs: dict ):
        
        global _SHADER
        if not _SHADER:
            _SHADER = self.compile_shader( f'#include "{SHADERPATH}"' )
        
        self.render_shader( _SHADER,
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
        outputs[ 'Color' ] = self.texture_targets[ 'COLOR' ]
        outputs[ 'Occlusion' ]  = self.texture_targets[ 'OCCLUSION' ]

NODE = EssentialsSky