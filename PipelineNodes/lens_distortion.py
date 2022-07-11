from pipeline_node import *

DISTORTION_SHADER = None

class EssentialsLensDistortion( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Distortion' : ( 'float', -0.1 ),
            'Dispersion' : ( 'float', 1.0 ),
            'Blur' : ( 'float', 0.2 ),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
        }
    
    def get_render_targets( self, resolution: tuple[int, int]) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )]
        }
    
    
    def render( self, inputs: dict, outputs: dict ):
        
        global DISTORTION_SHADER
        if not DISTORTION_SHADER:
            DISTORTION_SHADER = self.compile_shader( get_shader_source( 'LensDistortion.glsl' ))
        
        self.render_shader( DISTORTION_SHADER, self.get_render_target( 'MAIN' ),
            textures = { 'color_texture' : inputs[ 'Color' ] },
            uniforms = {
                'distortion' : inputs[ 'Distortion' ],
                'offset' : inputs[ 'Dispersion' ],
                'blur' : inputs[ 'Blur' ],
            }
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsLensDistortion