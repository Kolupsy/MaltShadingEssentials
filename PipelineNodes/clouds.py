from pipeline_node import *

CLOUD_SHADER = None

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
    
    def get_render_targets( self, resolution: tuple[int, int]) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )]
        }
    
    
    def render( self, inputs: dict, outputs: dict ):
        
        global CLOUD_SHADER
        if not CLOUD_SHADER:
            CLOUD_SHADER = self.compile_shader( 
                get_shader_source( 'Clouds.glsl' ),
                include_paths = [ get_shader_functions_path( )])
        
        self.render_shader( CLOUD_SHADER, self.get_render_target( 'MAIN' ),
            uniforms = {
                'main_cloud_strength' : inputs[ 'Main Clouds' ],
                'streak_cloud_strength' : inputs[ 'Streaky Clouds' ],
                'wind_speed' : inputs[ 'Wind Speed' ],
                'wind_angle' : inputs[ 'Wind Angle' ]
            }
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsClouds