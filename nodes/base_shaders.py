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

NODES = [ MaltNodeDiffuseShader, MaltNodeSpecularShader, MaltNodeGradientShading, MaltNodeEmission ]