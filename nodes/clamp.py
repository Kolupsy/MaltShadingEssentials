from .utils import *
from bpy.props import *

data_type_items = [
    ( 'FLOAT', '1', 'Clamp a single value' ),
    ( 'VEC2', '2', 'Clamp a UV' ),
    ( 'VEC3', '3', 'Clamp a vector' ),
    ( 'VEC4', '4', 'Clamp a color' ),
]

class MaltNodeClamp( EssentialsNode ):
    bl_idname = 'MaltNodeClamp'
    bl_label = 'Clamp'
    menu_category = 'CONVERTOR'
    default_width = 160

    data_type : EnumProperty( name = 'Data Type', items = data_type_items, update = lambda s,c:s.update_config( ))

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def get_name_pattern( self ):
        return{
            'FLOAT' : 'float',
            'VEC2' : 'uv',
            'VEC3' : 'vector',
            'VEC4' : 'color',
        }[ self.data_type ]

    def update_socket_visibility( self ):

        t = self.get_name_pattern( )
        for socket in list( self.inputs ) + list( self.outputs ):
            socket.enabled = t in socket.name

    def define_sockets( self ):
        return{
            'in_float' : I( 'float', 'Value', default = '0.0' ),
            'float_min' : I( 'float', 'Min', default = 0.0 ),
            'float_max' : I( 'float', 'Max', default = 1.0 ),
            'out_float' : O( 'float', 'Value' ),

            'in_uv' : I( 'vec2', 'UV', default = 'vec2( 0.0 )' ),
            'uv_min' : I( 'vec2', 'Min', default = ( 0.0, 0.0 )),
            'uv_max' : I( 'vec2', 'Max', default = ( 1.0, 1.0 )),
            'out_uv' : O( 'vec2', 'UV' ),

            'in_vector' : I( 'vec3', 'Vector', default = 'vec3( 0.0 )' ),
            'vector_min' : I( 'vec3', 'Min', subtype = 'Vector', default = ( 0.0, 0.0, 0.0 )),
            'vector_max' : I( 'vec3', 'Max', subtype = 'Vector', default = ( 1.0, 1.0, 1.0 )),
            'out_vector' : O( 'vec3', 'Vector' ),

            'in_color' : I( 'vec4', 'Color', default = 'vec4( 0.0, 0.0, 0.0, 1.0 )' ),
            'color_min' : I( 'vec4', 'Min', default = ( 0.0, 0.0, 0.0, 0.0 )),
            'color_max' : I( 'vec4', 'Max', default = ( 1.0, 1.0, 1.0, 1.0 )),
            'out_color' : O( 'vec4', 'Color' ),
        }
    
    def get_function( self ):
        t = self.get_name_pattern( )
        return f'out_{t} = clamp( in_{t}, {t}_min, {t}_max );\n'

    def draw_buttons( self, context, layout ):
        layout.prop_tabs_enum( self, 'data_type' )

NODES = [ MaltNodeClamp ]
