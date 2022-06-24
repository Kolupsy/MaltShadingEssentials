from .utils import *
from bpy.props import *

data_type_items = [
    ( 'FLOAT', '1', 'Mix between two single values' ),
    ( 'VEC2', '2', 'Mix between two UVs' ),
    ( 'VEC3', '3', 'Mix between two vectors' ),
    ( 'VEC4', '4', 'Mix between two colors' ),
]

class MaltNodeLerp( EssentialsNode ):
    bl_idname = 'MaltNodeLerp'
    bl_label = 'Lerp'
    menu_category = 'CONVERTOR'
    default_width = 160

    data_type : EnumProperty( name = 'Data Type', items = data_type_items, update = lambda s,c:s.update_config( ))

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def update_socket_visibility( self ):
        pattern = self.get_name_pattern( )
        for socket in list( self.inputs ) + list( self.outputs ):
            socket.enabled = pattern in socket.name or socket.name == 'mix_fac'

    def get_name_pattern( self ) -> str:
        return {
            'FLOAT': 'float',
            'VEC2' : 'uv',
            'VEC3' : 'vector',
            'VEC4' : 'color'
        }[ self.data_type ]

    def define_sockets( self ):
        return{
            'mix_fac' : I( 'float', 'Factor', default = 0.5 ),
            'in_float_1' : I( 'float', 'Value 1', default = 0.0 ),
            'in_float_2' : I( 'float', 'Value 2', default = 1.0 ),
            'out_float' : O( 'float', 'Value' ),
            'in_uv_1' : I( 'vec2', 'UV 1', default = ( 0.0, 0.0 )),
            'in_uv_2' : I( 'vec2', 'UV 2', default = ( 1.0, 1.0 )),
            'out_uv' : O( 'vec2', 'UV' ),
            'in_vector_1' : I( 'vec3', 'Vector 1', subtype = 'Vector', default = ( 0.0, 0.0, 0.0 )),
            'in_vector_2' : I( 'vec3', 'Vector 2', subtype = 'Vector', default = ( 1.0, 1.0, 1.0 )),
            'out_vector' : O( 'vec3', 'Vector' ),
            'in_color_1' : I( 'vec4', 'Color 1', default = ( 0.0, 0.0, 0.0, 0.0 )),
            'in_color_2' : I( 'vec4', 'Color 2', default = ( 1.0, 1.0, 1.0, 1.0 )),
            'out_color' : O( 'vec4', 'Color' ),
        }
    
    def get_function( self ):
        pattern = self.get_name_pattern( )
        first = f'in_{pattern}_1'
        second = f'in_{pattern}_2'
        output = f'out_{pattern}'
        return f'{output} = mix( {first}, {second}, mix_fac );'

    def draw_buttons( self, context, layout ):
        layout.prop_tabs_enum( self, 'data_type' )

NODES = [ MaltNodeLerp ]