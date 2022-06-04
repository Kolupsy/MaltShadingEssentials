from .utils import *
from bpy.props import *

class MaltNodePrimitive( EssentialsNode ):

    prim_type = ''
    prim_name = ''
    prim_subtype = ''
    menu_category = 'PRIMITIVES'

    def on_init( self ):
        self.inputs[ 'in_value' ].hide = True

    def define_sockets( self ):
        return{
            'in_value' : I( self.prim_type, self.prim_name, subtype = self.prim_subtype ),
            'out_value' : O( self.prim_type, self.prim_name )
        }
    
    def get_function( self ):
        return 'out_value = in_value;'
    
    def draw_buttons( self, context, layout ):
        c = layout.column( align = True )
        self.malt_parameters.draw_parameter( c, 'in_value', '', is_node_socket = True )


def make_primitive_type( prim_type, prim_name, prim_subtype ):
    clss_name = f'MaltNode{prim_name}'
    clss = type( clss_name, ( MaltNodePrimitive, ), {
        'bl_idname' : clss_name,
        'bl_label' : prim_name,
        'prim_type' : prim_type,
        'prim_name' : prim_name,
        'prim_subtype' : prim_subtype,
    })
    return clss

types = [
    ( 'float', 'Float', '' ),
    ( 'int', 'Int', '' ),
    ( 'bool', 'Bool', '' ),
    ( 'vec2', 'UV', '' ),
    ( 'vec3', 'Vector', 'Vector' ),
    ( 'vec4', 'Color', 'Color' ),
    ( 'sampler1D', 'Ramp', '' ),
    ( 'sampler2D', 'Texture', '' ),
]

NODES = [ make_primitive_type( t, n, s ) for t, n, s in types ]