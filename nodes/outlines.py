from .utils import *

class MaltNodeOutlines( EssentialsNode ):
    bl_idname = 'MaltNodeOutlines'
    bl_label = 'Outlines'
    menu_category = 'TEXTURE'

    def define_sockets( self ):
        return{
            'width' : I( 'float', 'Thickness', default = 0.3 ),
            'depth' : I( 'float', 'Inner Lines', default = 0.8 ),
            'normal' : I( 'float', 'Details', default = 0.5 ),
            'scale' : I( 'float', 'Noise Scale', default = 2.5 ),
            'bias' : I( 'float', 'Bias', default = 0.7 ),

            'tapered' : O( 'float', 'Tapered Lines' ),
            'noisy' : O( 'float', 'Noisy Lines' )
        }
    
    def get_function( self ): #TODO
        f = ''
        f += 'tapered = tapered_lines( width, depth, normal );\n'
        f += 'noisy = noisy_lines( width, depth, normal, scale, bias );\n'
        return f
    
NODES = [ MaltNodeOutlines ]