
from .utils import *

class MaltNodeCurveViewMapping( EssentialsNode ):
    bl_idname = 'MaltNodeCurveViewMapping'
    bl_label = 'Curve View Mapping'
    menu_category = 'INPUT'
    default_width = 160

    def define_sockets( self ):
        return{
            'tangent' : I( 'vec3', 'Tangent', default = 'compute_tangent( UV[0] ).xyz' ),
            'incoming' : I( 'vec3', 'Incoming', default = 'incoming_vector( )' ),
            'normal' : I( 'vec3', 'Normal', default = 'NORMAL' ),
            'result' : O( 'vec2', 'UV' ),
            'curve_facing' : O( 'float', 'Facing' ) 
        }
    
    def get_function( self ):
        return 'curve_view_mapping( tangent, incoming, normal, result, curve_facing );\n'

NODES = [ MaltNodeCurveViewMapping ]