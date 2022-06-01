from .utils import *

class MaltNodeBrightContrast( EssentialsNode ):
    bl_idname = 'MaltNodeBrightContrast'
    bl_label = 'Bright/Contrast'
    menu_category = 'COLOR'

    def define_sockets( self ):
        return{
            'color' : I( 'vec4', 'Color', default = ( 1.0, 1.0, 1.0, 1.0 )),
            'brightness' : I( 'float', 'Bright', default = 0.0 ),
            'contrast' : I( 'float', 'Contrast', default = 0.0 ),
            'result' : O( 'vec4', 'Color' ),
        }
    
    def get_function( self ):
        return 'result = brightness_contrast( color, brightness, contrast );\n'
    
NODES = [ MaltNodeBrightContrast ]