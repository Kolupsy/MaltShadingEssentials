import pathlib
from pipeline_node import *

_SHADER = None

SHADERPATH = str( pathlib.Path( __file__ ).parent.parent.joinpath( 'Shaders', 'Clouds.glsl' ))

class EssentialsClouds( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Main Clouds' : ( 'float', 0.65 ),
            'Streaky Clouds' : ( 'float', 0.3 ),
            'Wind Speed' : ( 'float', 0.05 ),
            'Wind Angle' : ( 'float', 0.0 ),
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
            uniforms = {
                'main_cloud_strength' : inputs[ 'Main Clouds' ],
                'streak_cloud_strength' : inputs[ 'Streaky Clouds' ],
                'wind_speed' : inputs[ 'Wind Speed' ],
                'wind_angle' : inputs[ 'Wind Angle' ]
            }
        )
        outputs[ 'Color' ] = self.texture_targets[ 'COLOR' ]

NODE = EssentialsClouds