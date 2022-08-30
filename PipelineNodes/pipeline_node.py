from Malt.PipelineNode import PipelineNode
from Malt.PipelineParameters import Parameter, Type
from Malt.GL.Texture import Texture
from Malt.GL.GL import GL_RGBA16F, GL_RGBA32F, GL_R16F, GL_RG16F, GL_RGB16F
from Malt.GL.Shader import Shader
from Malt.GL.RenderTarget import RenderTarget
from Malt.Render import Lighting

from typing import Any
from dataclasses import dataclass

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
        'str' : Parameter( default, Type.STRING ),
        'OTHER' : Parameter( default, Type.OTHER ),
    }[ glsl_type ]

class TextureFormat:

    RGBA16F = GL_RGBA16F
    RGBA32F = GL_RGBA32F
    R16F = GL_R16F
    RG16F = GL_RG16F
    RGB16F = GL_RGB16F

@dataclass
class TextureTarget:

    name:str
    texture_format:str
    resolution:tuple[int, int]

    def get_real_resolution( self ):
        return (
            max( 0, int( self.resolution[0])),
            max( 0, int( self.resolution[1]))
        )

    def get_texture( self ):
        return Texture( self.get_real_resolution( ), self.texture_format )

class CustomPipelineNode( PipelineNode ):
    
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
        self.texture_targets = {}
        self.render_targets = {}

    def compile_shader( self, shader_code, include_paths = [], defines = [] ) -> Shader:
        return self.pipeline.compile_shader_from_source( source = shader_code, include_paths = include_paths, defines = defines )
    
    def get_render_targets( self, resolution:tuple[int,int], inputs ) -> dict[str,list[TextureTarget]]:
        return {}
    
    def setup_render_targets( self, resolution, inputs ):
        self.resolution = resolution

        for name, textures in self.get_render_targets( resolution, inputs ).items( ):

            render_textures = { t.name : t.get_texture( ) for t in textures }

            self.texture_targets[name] = render_textures
            self.render_targets[ name ] = RenderTarget([*render_textures.values( )])
    
    def get_output( self, render_target_name, texture_target_name ):
        return self.texture_targets[ render_target_name ][ texture_target_name ]

    def get_render_target( self, name ):
        return self.render_targets[ name ]
    
    def setup_lights_buffer( self, shader:Shader, scene:'Scene' ) -> None:
        lights_buffer = Lighting.get_lights_buffer( )
        lights_buffer.load( scene, 4, 0.9, 100.0, 1, 1.0 )
        lights_buffer.shader_callback( shader )

    def render_shader( self, shader:Shader, target, textures:dict = {}, uniforms:dict = {} ) -> None:
        
        for tex_key, tex_value in textures.items( ):
            shader.textures[ tex_key ] = tex_value
        
        for uni_key, uni_value in uniforms.items( ):
            if not uni_key in shader.uniforms.keys( ):
                print( f'Uniform {uni_key} unavailable!' )
                continue
            shader.uniforms[ uni_key ].set_value( uni_value )
        
        self.pipeline.common_buffer.shader_callback( shader )
        self.pipeline.draw_screen_pass( shader, target )

    def render( self, inputs:dict, outputs:dict ) -> None:
        pass

    def execute( self, parameters ):
        inputs = parameters[ 'IN' ]
        outputs = parameters[ 'OUT' ]

        if self.pipeline.resolution != self.resolution:
            self.setup_render_targets( self.pipeline.resolution, inputs )
        
        self.render( inputs, outputs )

template_screen_shader = '''

#include "Common.glsl"

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

#INSERT_SCREEN_SHADER

#endif
'''

def generate_source( code:str ):
    return template_screen_shader.replace( '#INSERT_SCREEN_SHADER', code )

def scale_res( resolution:tuple[int,int], scale:float):
    return(
        resolution[0] * scale,
        resolution[1] * scale,
    )

def get_shader_source( shader_file_name: str ) -> str:
    import pathlib
    path = str( pathlib.Path( __file__ ).parent.parent.joinpath( 'Shaders', shader_file_name ))
    return f'#include "{path}"'

def get_shader_functions_path( ) -> str:
    import pathlib
    return str( pathlib.Path( __file__ ).parent.parent.joinpath( 'ShaderFunctions' ))

class DummyPipelineNode( PipelineNode ):

    @classmethod
    def reflect( cls ):
        reflection = super( ).reflect( )
        reflection[ 'meta' ][ 'internal' ] = True
        return reflection

__all__ = [ 'Any', 'CustomPipelineNode', 'TextureTarget', 'TextureFormat', 'generate_source', 'get_shader_source', 'get_shader_functions_path', 'scale_res' ]
NODE = DummyPipelineNode