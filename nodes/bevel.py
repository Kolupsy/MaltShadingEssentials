from .utils import *
from bpy.props import *

bevel_mode_items = [
    ( 'SOFT', 'Soft', 'Soft Bevel' ),
    ( 'HARD', 'Hard', 'Hard Bevel' )
]

class MaltNodeBevel( EssentialsNode ):
    bl_idname = 'MaltNodeBevel'
    bl_label = 'Bevel'
    menu_category = 'VECTOR'

    bevel_mode : EnumProperty( name = 'Bevel Mode', items = bevel_mode_items, update = lambda s,c:s.update_config( ))

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )

    def update_socket_visibility( self ):
        is_soft = self.bevel_mode == 'SOFT'
        self.inputs[ 'exponent' ].enabled = is_soft
        self.inputs[ 'max_dot' ].enabled = not is_soft

    def define_sockets( self ):
        return{
            'radius' : I( 'float', 'Radius', default = 0.015 ),
            'exponent' : I( 'float', 'Exponent', default = 2.0 ),
            'max_dot' : I( 'float', 'Max Dot', default = 0.75 ),
            'samples' : I( 'int', 'Samples', default = 64 ),
            'only_self' : I( 'bool', 'Only Self' ),
            'out_normal' : O( 'vec3', 'Normal' ),
        }
    
    def get_function( self ):
        f = '#ifdef NPR_FILTERS_ACTIVE\n'
        f += 'uint id = texture( IN_ID, screen_uv( ))[0];\n'
        if self.bevel_mode == 'SOFT':
            f += 'out_normal = bevel( IN_NORMAL_DEPTH, IN_NORMAL_DEPTH, 3, id, only_self, IN_ID, 0, samples, radius, exponent, false, 1 );\n'
        else:
            f += 'out_normal = bevel( IN_NORMAL_DEPTH, IN_NORMAL_DEPTH, 3, id, only_self, IN_ID, 0, samples, radius, 1.0, true, max_dot );\n'
        f += '#endif\n'
        return f
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'bevel_mode', text = '' )

NODES = [ MaltNodeBevel ]