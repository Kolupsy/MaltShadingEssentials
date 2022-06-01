from .utils import *
from bpy.props import *

noise_rna = bpy.types.ShaderNodeTexWhiteNoise.bl_rna

noise_dimensions_items = enum_from_rna( noise_rna, 'noise_dimensions' )

class MaltNodeTexWhiteNoise( EssentialsNode ):
    bl_idname = 'MaltNodeTexWhiteNoise'
    bl_label = 'White Noise'
    menu_category = 'TEXTURE'

    noise_dimensions : EnumProperty( name = 'Dimensions', items = noise_dimensions_items, update = lambda s,c:s.update_config( ))

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )

    def update_socket_visibility( self ):
        t = self.noise_dimensions
        self.inputs[ 'w' ].enabled = t == '1D'
        self.inputs[ 'uv' ].enabled = t == '2D'
        self.inputs[ 'vector' ].enabled = t == '3D'
        self.inputs[ 'color' ].enabled = t == '4D'

    def define_sockets( self ):
        return{
            'w' : I( 'float', 'W' ),
            'uv' : I( 'vec2', 'UV', default = 'UV[0]' ),
            'vector' : I( 'vec3', 'Vector', default = 'POSITION' ),
            'color' : I( 'vec4', 'Color', default = 'vec4( POSITION, 1.0 )' ),
            'noise' : O( 'vec4', 'Noise' )
        }
    
    def get_function( self ):
        return{
            '1D' : 'noise = texture_white_noise_1d( w );',
            '2D' : 'noise = texture_white_noise_2d( uv );',
            '3D' : 'noise = texture_white_noise_3d( vector );',
            '4D' : 'noise = texture_white_noise_4d( color );',
        }[ self.noise_dimensions ]
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'noise_dimensions', text = '' )

NODES = [ MaltNodeTexWhiteNoise ]