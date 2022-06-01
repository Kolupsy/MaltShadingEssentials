from .utils import *
from bpy.props import *

gradient_rna = bpy.types.ShaderNodeTexGradient.bl_rna

gradient_type_items = enum_from_rna( gradient_rna, 'gradient_type' )

class MaltNodeTexGradient( EssentialsNode ):
    bl_idname = 'MaltNodeTexGradient'
    bl_label = 'Gradient Texture'
    menu_category = 'TEXTURE'

    gradient_type : EnumProperty( name = 'Gradient Type', items = gradient_type_items, update = lambda s,c:s.update_config( ) )

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )

    def update_socket_visibility( self ):
        t = self.gradient_type
        self.inputs[ 'w' ].enabled = t in [ 'LINEAR', 'QUADRATIC', 'EASING']
        self.inputs[ 'uv' ].enabled = t in [ 'DIAGONAL', 'RADIAL' ]
        self.inputs[ 'vector' ].enabled = t in [ 'SPHERICAL', 'QUADRATIC_SPHERE' ]

    def define_sockets( self ):
        return{
            'w' : I( 'float', 'W', default = 'UV[0].x' ),
            'uv' : I( 'vec2', 'UV', default = 'UV[0]' ),
            'vector' : I( 'vec3', 'Vector', default = 'object_coords( )' ),
            'gradient' : O( 'float', 'Gradient' ),
        }
    
    def get_function( self ):
        return{
            'LINEAR' : 'gradient = texture_gradient_linear( w );',
            'QUADRATIC' : 'gradient = texture_gradient_quadratic( w );',
            'EASING' : 'gradient = texture_gradient_easing( w );',
            'DIAGONAL' : 'gradient = texture_gradient_diagonal( uv );',
            'SPHERICAL' : 'gradient = texture_gradient_spherical( vector );',
            'QUADRATIC_SPHERE' : 'gradient = texture_gradient_quadratic_sphere( vector );',
            'RADIAL' : 'gradient = texture_gradient_radial( uv );'
        }[ self.gradient_type ]
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'gradient_type', text = '' )

NODES = [ MaltNodeTexGradient ]