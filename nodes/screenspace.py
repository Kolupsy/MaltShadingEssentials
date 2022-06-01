from .utils import *

class MaltNodeScreenSpace( EssentialsNode ):
    bl_idname = 'MaltNodeScreenSpace'
    bl_label = 'Screen Space'
    menu_category = 'INPUT'
    default_width = 150

    def define_sockets( self ):
        return{
            'flat_uv' : O( 'vec2', 'Flat' ),
            'projected' : O( 'vec2', 'Projected' ),
            'matcap' : O( 'vec2', 'Matcap UV' ),
            'normal_space' : O( 'vec2', 'Normal Space' ),
            'screen' : O( 'vec2', 'Screen UV' ),
        }
    
    def get_function( self ):
        f = 'screenspace_info( flat_uv, projected, matcap, screen );\n'
        f += 'normal_space = matcap * vec2(2) - vec2( 1 );'
        return f
    
NODES = [ MaltNodeScreenSpace ]