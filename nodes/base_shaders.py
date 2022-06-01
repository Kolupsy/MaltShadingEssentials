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

    gradient_type : EnumProperty( name = 'Gradient Type', items = gradient_type_items, update = lambda s, c:s.update_gradient_type( ))

    def update_gradient_type( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def update_socket_visibility( self ):
        self.inputs[ 'roughness' ].enabled = self.gradient_type == 'SPECULAR'

    def define_sockets( self ):
        return{
            'roughness' : I( 'float', 'Roughness', default = 0.8 ),
            'normal' : I( 'vec3', 'Normal', subtype = 'Normal', default = 'NORMAL' ),
            'light_group' : I( 'int', 'Group', default = 1 ),
            'shadows' : I( 'bool', 'Shadows', default = True ),
            'self_shadows' : I( 'bool', 'Self Shadows', default = True ),
            'gradient' : O( 'float', 'Gradient' )
        }
    
    def get_function( self ):
        f = {
            'DIFFUSE':'gradient = rgb_to_hsv( diffuse_shading( POSITION, normal, light_group, shadows, self_shadows )).z;\n',
            'SPECULAR':'gradient = rgb_to_hsv( specular_shading( POSITION, normal, roughness, light_group, shadows, self_shadows )).z;\n',
        }[ self.gradient_type ]
        return f
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'gradient_type', text = '' )
    
    def draw_label( self ):
        return next( x[1] for x in gradient_type_items if self.gradient_type == x[0] ) + ' Gradient'

NODES = [ MaltNodeDiffuseShader, MaltNodeSpecularShader, MaltNodeGradientShading ]