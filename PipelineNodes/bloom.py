from Malt.PipelineNode import PipelineNode
from Malt.PipelineParameters import Parameter, Type
from Malt.GL.Texture import Texture
from Malt.GL.GL import GL_RGBA16F
from Malt.GL.RenderTarget import RenderTarget

import pathlib

_SHADER = None

BLOOMPATH = str( pathlib.Path( __file__ ).parent.parent.joinpath( 'Shaders', 'Bloom.glsl' ))

class CustomBloomPass( PipelineNode ):

    def __init__( self, pipeline ):
        PipelineNode.__init__( self, pipeline )
        self.resolution = None
    
    @classmethod
    def reflect_inputs( cls ):
        inputs = {}
        inputs[ 'Color' ] = Parameter( '', Type.TEXTURE )
        return inputs
    
    @classmethod
    def reflect_outputs( cls ):
        outputs = {}
        outputs[ 'Color' ] = Parameter( '', Type.TEXTURE )
        return outputs
    
    @staticmethod
    def get_pass_type( ):
        return 'Screen.SCREEN_SHADER'
    
    def setup_render_targets( self, resolution ):
        self.t_color = Texture( resolution, GL_RGBA16F )
        self.fbo_color = RenderTarget([ self.t_color ])
    
    def execute( self, parameters ):
        inputs = parameters[ 'IN' ]
        outputs = parameters[ 'OUT' ]

        if self.pipeline.resolution != self.resolution:
            self.setup_render_targets( self.pipeline.resolution )
            self.resolution = self.pipeline.resolution
            self.texture_targets = {}
            self.texture_targets[ 'Color' ] = Texture( self.pipeline.resolution, GL_RGBA16F )
            self.render_target = RenderTarget([*self.texture_targets.values( )])
        
        global _SHADER
        if _SHADER is None:
            _SHADER = self.pipeline.compile_shader_from_source( f'#include "{BLOOMPATH}"' )
            _SHADER.textures[ 'color_texture' ] = inputs[ 'Color' ]
            self.pipeline.common_buffer.shader_callback( _SHADER )
            self.pipeline.draw_screen_pass( _SHADER, self.fbo_color )
            
            outputs[ 'Color' ] = self.texture_targets[ 'Color' ]

NODE = CustomBloomPass