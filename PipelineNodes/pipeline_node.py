from Malt.PipelineNode import PipelineNode
from Malt.PipelineParameters import Parameter, Type
from Malt.GL.Texture import Texture
from Malt.GL.GL import GL_RGBA16F
from Malt.GL.Shader import Shader
from Malt.GL.RenderTarget import RenderTarget
from Malt.Render import Lighting

from typing import Any

def get_param( glsl_type:str, default:Any ) -> Parameter:
    return{
        'int' : Parameter( default, Type.INT ),
        'float' : Parameter( default, Type.FLOAT ),
        'sampler2D' : Parameter( default, Type.TEXTURE ),
        'sampler2d' : Parameter( default, Type.TEXTURE ),
        'bool' : Parameter( default, Type.BOOL ),
        'vec2' : Parameter( default, Type.FLOAT, size = 2 ),
        'vec3' : Parameter( default, Type.FLOAT, size = 3 ),
        'vec4' : Parameter( default, Type.FLOAT, size = 4 ),
        'OTHER' : Parameter( default, Type.OTHER ),
    }[ glsl_type ]

class PipelineNodeExtended( PipelineNode ):
    
    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return {}
    
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return {}

    @classmethod
    def reflect_inputs( cls ) -> dict[str,Parameter]:
        return { key: get_param( value[0], value[1]) for key, value in cls.static_inputs( ).items( )}
    
    @classmethod
    def reflect_outputs( cls ) -> dict:
        return { key: get_param( value[0], value[1]) for key, value in cls.static_outputs( ).items( )}
    
    def __init__( self, pipeline ):
        PipelineNode.__init__( self, pipeline )
        self.resolution = None
    
    def compile_shader_from_source( self, source, include_paths = [], defines = []) -> Shader:
        return self.pipeline.compile_shader_from_source( source = source, include_paths = include_paths, defines = defines )

    def compile_shader( self, shader_code ) -> Shader:
        return self.compile_shader_from_source( shader_code )
    
    def get_texture_targets( self ) -> list[str]:
        return []
    
    def setup_render_targets( self, resolution ):
        self.resolution = resolution
        self.texture_targets = {}
        for target_name in self.get_texture_targets( ):
            self.texture_targets[ target_name ] = Texture( resolution, GL_RGBA16F )
        self.render_target = RenderTarget([*self.texture_targets.values( )])
    
    def setup_lights_buffer( self, shader:Shader, scene:'Scene' ) -> None:
        lights_buffer = Lighting.get_lights_buffer( )
        lights_buffer.load( scene, 4, 0.9, 100.0, 1, 1.0 )
        lights_buffer.shader_callback( shader )

    def render_shader( self, shader:Shader, textures:dict = {}, uniforms:dict = {} ) -> None:
        
        for tex_key, tex_value in textures.items( ):
            shader.textures[ tex_key ] = tex_value
        
        for uni_key, uni_value in uniforms.items( ):
            if not uni_key in shader.uniforms.keys( ):
                print( f'Uniform {uni_key} unavailable!' )
                continue
            shader.uniforms[ uni_key ].set_value( uni_value )
        
        self.pipeline.common_buffer.shader_callback( shader )
        self.pipeline.draw_screen_pass( shader, self.render_target )

    def render( self, inputs:dict, outputs:dict ) -> None:
        pass

    def execute( self, parameters ):
        inputs = parameters[ 'IN' ]
        outputs = parameters[ 'OUT' ]

        if self.pipeline.resolution != self.resolution:
            self.setup_render_targets( self.pipeline.resolution )
        
        self.render( inputs, outputs )

class CustomPipelineNode( PipelineNodeExtended ):
    '''Class Template for custom Pipeline nodes:
    Override:
        static_inputs
        static_outputs
        render
        get_texture_targets
    '''

    @classmethod
    def static_inputs( cls ) -> dict[str, tuple[str, Any]]:
        return super( ).static_inputs( )
    
    @classmethod
    def static_outputs( cls ) -> dict[str, tuple[str, Any]]:
        return super( ).static_outputs( )
    
    def render( self, inputs: dict, outputs: dict ):
        return super().render( inputs, outputs )
    
    def get_texture_targets( self ) -> list[str]:
        return super( ).get_texture_targets( )

class DummyPipelineNode( PipelineNode ):

    @classmethod
    def reflect( cls ):
        reflection = super( ).reflect( )
        reflection[ 'meta' ][ 'internal' ] = True
        return reflection

__all__ = [ 'Any', 'CustomPipelineNode' ]
NODE = DummyPipelineNode