from .utils import *

class MaltNodeVectorDistortion( EssentialsNode ):
    bl_idname = 'MaltNodeVectorDistortion'
    bl_label = 'Vector Distortion'
    menu_category = 'VECTOR'
    default_width = 160

    def define_sockets( self ):
        return{
            'vector' : I( 'vec3', 'Vector', subtype = 'Vector', default = 'POSITION' ),
            'distortion' : I( 'vec3', 'Distortion', subtype = 'Vector', default = 'vec3( 0.5 )' ),
            'factor' : I( 'float', 'Factor', default = 0.5 ),
            'result' : O( 'vec3', 'Vector' )
        }
    
    def get_function( self ):
        return 'result = vector_distortion( vector, distortion, factor );\n'

NODES = [ MaltNodeVectorDistortion ]