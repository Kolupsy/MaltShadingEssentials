from Malt.PipelineNode import PipelineNode
from Malt.PipelineParameters import Parameter, Type
from Malt.GL.Texture import Texture
from Malt.GL.GL import GL_RGBA16F
from Malt.GL.RenderTarget import RenderTarget

import pathlib

_SHADER = None

SHADERPATH = str( pathlib.Path( __file__ ).parent.parent.joinpath( 'Shaders', 'LensFlare.glsl' ))

class EssentialsLensFlare( PipelineNode ):

    def __init__( self, pipeline ):
        PipelineNode.__init__( self, pipeline )
        self.resolution = None
    
    @classmethod
    def reflect_inputs( cls ):
        return {
            'Color' : Parameter( '', Type.TEXTURE ),
            'Rot X' : Parameter( 0.0, Type.FLOAT ),
            'Rot Y' : Parameter( 0.0, Type.FLOAT ),
            'Rot Z' : Parameter( 0.0, Type.FLOAT ),
        }
    
    @classmethod
    def reflect_outputs( cls ):
        return {
            'Color' : Parameter( '', Type.TEXTURE )
        }
    
    def setup_render_targets( self, resolution ):
        self.resolution = resolution
        self.texture_targets = {}
        self.texture_targets[ 'COLOR' ] = Texture( resolution, GL_RGBA16F )
        self.render_target = RenderTarget([*self.texture_targets.values( )])
    
    def execute( self, parameters ):
        inputs = parameters[ 'IN' ]
        outputs = parameters[ 'OUT' ]

        if self.pipeline.resolution != self.resolution:
            self.setup_render_targets( self.pipeline.resolution )
        
        global _SHADER
        if _SHADER is None:
            self.compile_shader( )
        
        _SHADER.textures[ 'color_texture' ] = inputs[ 'Color' ]
        _SHADER.uniforms[ 'euler_rot' ].set_value(( inputs[ 'Rot X' ], inputs[ 'Rot Y' ], inputs[ 'Rot Z']))
        self.pipeline.common_buffer.shader_callback( _SHADER )
        self.pipeline.draw_screen_pass( _SHADER, self.render_target )
            
        outputs[ 'Color' ] = self.texture_targets[ 'COLOR' ]

    def compile_shader_from_source( self, source, include_paths = [], defines = []):
        return self.pipeline.compile_shader_from_source( source = source, include_paths = include_paths, defines = defines )

    def compile_shader( self ):
        global _SHADER
        _SHADER = self.compile_shader_from_source( f'#include "{SHADERPATH}"' )

NODE = EssentialsLensFlare