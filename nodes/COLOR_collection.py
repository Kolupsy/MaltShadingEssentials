from bpy.props import *
from .utils import *

class MaltNodeHueSaturation( EssentialsNode ):
    bl_idname = 'MaltNodeHueSaturation'
    bl_label = 'Hue Saturation Value'
    menu_category = 'COLOR'
    default_width = 165

    def define_sockets( self ):
        return {
            'h' : I( 'float', 'H', default = 0.5 ),
            's' : I( 'float', 'S', default = 1.0 ),
            'v' : I( 'float', 'V', default = 1.0 ),
            'fac' : I( 'float', 'Fac', default = 1.0 ),
            'invert' : I( 'bool', 'Invert', default = 0 ),
            'color' : I( 'vec4', 'Color', subtype = 'Color' ),
            'result' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        return 'hue_saturation_value( h, s, v, fac, invert, color, result );\n'

class MaltNodeGamma( EssentialsNode ):
    bl_idname = 'MaltNodeGamma'
    bl_label = 'Gamma'
    menu_category = 'COLOR'

    def define_sockets( self ):
        return{
            'color' : I( 'vec4', 'Color', default = ( 1.0, 1.0, 1.0, 1.0 )),
            'gamma' : I( 'float', 'Gamma', default = 1.0 ),
            'result' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        return 'result = gamma_correction( color, gamma );\n'

class MaltNodeInvert( EssentialsNode ):
    bl_idname = 'MaltNodeInvert'
    bl_label = 'Invert'
    menu_category = 'COLOR'

    def define_sockets( self ):
        return{
            'color' : I( 'vec4', 'Color', default = ( 0.0, 0.0, 0.0, 1.0 )),
            'fac' : I( 'float', 'Fac', default = 1.0 ),
            'result' : O( 'vec4', 'Color' ),
        }
    
    def get_function( self ):
        return 'result = color_invert( color, fac );'

NODES = [ MaltNodeHueSaturation, MaltNodeGamma, MaltNodeInvert ]