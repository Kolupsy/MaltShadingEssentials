from .utils import *
from bpy.props import *

outline_mode_items = [
    ('TAPERED', 'Tapered', 'Tapered outlines based on object bounds, depth and normal discontinuities' ),
    ('NOISY', 'Noisy', 'Based on tapered lines with additional noise options' )
]

class MaltNodeOutlines( EssentialsNode ):
    bl_idname = 'MaltNodeOutlines'
    bl_label = 'Outlines'
    menu_category = 'TEXTURE'

    outline_mode : EnumProperty( name = 'Outline Mode', items = outline_mode_items, update = lambda s,c:s.update_config( ))
    show_id_input : BoolProperty( name = 'Show ID Input', default = False, update = socket_update )

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def update_socket_visibility( self ):
        m = self.outline_mode
        self.inputs[ 'scale' ].enabled = m == 'NOISY'
        self.inputs[ 'bias' ].enabled = m == 'NOISY'
        self.inputs[ 'id' ].enabled = self.show_id_input

    def define_sockets( self ):
        return{
            'width' : I( 'float', 'Thickness', default = 0.3 ),
            'depth' : I( 'float', 'Inner Lines', default = 0.8 ),
            'normal' : I( 'float', 'Details', default = 0.5 ),
            'scale' : I( 'float', 'Noise Scale', default = 2.5 ),
            'bias' : I( 'float', 'Bias', default = 0.7 ),
            'id' : I( 'vec4', 'ID Bounds', subtype = 'Vector', default = ( 1.0, 1.0, 1.0, 1.0 )),

            'outlines' : O( 'float', 'Outline' )
        }
    
    def get_function( self ):
        f = {
            'TAPERED' : 'outlines = tapered_lines( width, depth, normal, id );',
            'NOISY' : 'outlines = noisy_lines( width * 2, depth, normal, id, scale, bias );',
        }[ self.outline_mode ]
        return f
    
    def draw_buttons( self, context, layout ):
        row = layout.row( align = True )
        row.prop( self, 'outline_mode', text = '' )
        row.prop( self, 'show_id_input', text = '', icon = 'PREFERENCES' )
    
NODES = [ MaltNodeOutlines ]