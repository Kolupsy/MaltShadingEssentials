from .utils import *

class MaltNodeVectorAngle( EssentialsNode ):
    bl_idname = 'MaltNodeVectorAngle'
    bl_label = 'Vector Angle'
    menu_category = 'VECTOR'

    def define_sockets( self ):
        return {
            'vector' : I( 'vec2', 'Vector', default = ( 0.0, 0.1 )),
            'angle' : O( 'float', 'Angle' ),
            'continuous' : O( 'float', 'Continuous Angle' ),
        }
    
    def get_function( self ):
        f = 'angle = vector_angle_2D( vector );\n'
        f += 'continuous = vector_angle_2D_continuous( vector );\n'
        return f

NODES = [ MaltNodeVectorAngle ]