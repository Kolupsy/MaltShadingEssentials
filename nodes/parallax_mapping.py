from .utils import *

class MaltNodeParallaxMapping( EssentialsNode ):
    bl_idname = 'MaltNodeParallaxMapping'
    bl_label = 'Parallax Mapping'
    menu_category = 'INPUT'

    def define_sockets( self ):
        return{
            'position' : I( 'vec3', 'Position', default = 'POSITION' ),
            'tangent' : I( 'vec3', 'Tangent', default = 'compute_tangent( UV[0]).xyz' ),
            'normal' : I( 'vec3', 'Normal', default = 'NORMAL' ),
            'depth' : I( 'float', 'Depth', default = -0.1 ),
            'vector' : O( 'vec3', 'Vector' )
        }
    
    def get_function( self ):
        return 'vector = parallax_mapping( position, tangent, normal, depth );\n'

NODES = [ MaltNodeParallaxMapping ]