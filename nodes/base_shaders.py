from .utils import *
from bpy.props import *

class BaseShaderNode( EssentialsNode ):
    menu_category = 'SHADER'
    default_width = 190

class MaltNodeDiffuseShader( BaseShaderNode ):
    bl_idname = 'MaltNodeDiffuseShader'
    bl_label = 'Diffuse'

    def define_sockets( self ):
        return{
            'base_color' : I( 'vec4', 'Base Color', default = ( 0.8, 0.8, 0.8, 1.0 )),
            'normal' : I( 'vec3', 'Normal', subtype = 'Normal', default = 'NORMAL' ),
            'light_group' : I( 'int', 'Group', default = 1 ),
            'shadows' : I( 'bool', 'Shadows', default = True ),
            'self_shadows' : I( 'bool', 'Self Shadows', default = True ),
            'color' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        return 'color = diffuse_shader( base_color, normal, light_group, shadows, self_shadows );'

class MaltNodeSpecularShader( BaseShaderNode ):
    bl_idname = 'MaltNodeSpecularShader'
    bl_label = 'Specular'

    def define_sockets( self ):
        return{
            'base_color' : I( 'vec4', 'Base Color', default = ( 0.8, 0.8, 0.8, 1.0 )),
            'roughness' : I( 'float', 'Roughness', default = 0.8 ),
            'normal' : I( 'vec3', 'Normal', subtype = 'Normal', default = 'NORMAL' ),
            'light_group' : I( 'int', 'Group', default = 1 ),
            'shadows' : I( 'bool', 'Shadows', default = True ),
            'self_shadows' : I( 'bool', 'Self Shadows', default = True ),
            'color' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        return 'color = specular_shader( base_color, roughness, normal, light_group, shadows, self_shadows );'

gradient_type_items = [
    ( 'DIFFUSE', 'Diffuse', 'Diffuse Gradient Shading' ),
    ( 'SPECULAR', 'Specular', 'Specular Gradient Shading' ),
]

class MaltNodeGradientShading( BaseShaderNode ):
    bl_idname = 'MaltNodeGradientShading'
    bl_label = 'Gradient'

    def define_sockets( self ):
        return{
            'position' : I( 'vec3', 'Position', default = 'POSITION' ),
            'normal' : I( 'vec3', 'Normal', default = 'NORMAL' ),
            'light_group' : I( 'int', 'Group', default = 1 ),
            'shadows' : I( 'bool', 'Shadows', default = True ),
            'self_shadows' : I( 'bool', 'Self Shadows', default = 1 ),
            'gradient' : O( 'vec3', 'Gradient' )
        }
    
    def get_function( self ):
        return 'gradient = diffuse_half_shading( position, normal, light_group, shadows, self_shadows );\n'

class MaltNodeEmission( BaseShaderNode ):
    bl_idname = 'MaltNodeEmission'
    bl_label = 'Emission'

    def define_sockets( self ):
        return{
            'color' : I( 'vec4', 'Color', default = ( 0.8, 0.8, 0.8, 1 )),
            'bright' : I( 'float', 'Brightness', default = 1.0 ),
            'mask' : I( 'float', 'Mask', default = 'float( 1.0 )' ),
            'result' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        return 'result = emission( color, bright, mask );'

from typing import Any

class MaltNodeBloomPass( EssentialsPipelineNode ):
    bl_idname = 'MaltNodeBloomPass'
    bl_label = 'Bloom Pass'
    menu_category = 'SHADER'

    SHADER = None

    @classmethod
    def static_inputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Color' : ( 'sampler2D', '' ),
        }
    @classmethod
    def static_outputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Color' : ( 'sampler2D', '' ),
        }
    
    def get_texture_targets(self) -> list[str]:
        return [ 'OUT_COLOR' ]
    
    def render( self, inputs: dict, outputs: dict ):
        
        if not self.SHADER:
            self.SHADER = self.compile_shader( self.get_shader_code( ))
        outputs[ 'Color' ] = self.texture_targets[ 'OUT_COLOR' ]
    
    def get_shader_code( self ):
        return '''
#include "Common.glsl"

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER
layout (location = 0) out vec4 OUTPUT1;
void main()
{
    PIXEL_SETUP_INPUT();

    OUTPUT1 = vec4(0.0,0.1,0.1,1);
}
#endif
'''

NODES = [ MaltNodeDiffuseShader, MaltNodeSpecularShader, MaltNodeGradientShading, MaltNodeEmission ]