from bpy.props import *
from .utils import *

class MaltNodeLayerWeight( EssentialsNode ):
    bl_idname = 'MaltNodeLayerWeight'
    bl_label = 'Layer Weight'
    menu_category = 'INPUT'

    def define_sockets( self ):
        return {
            'blend' : I( 'float', 'Blend', default = 0.5 ),
            'normal' : I( 'vec3', 'Normal', default = 'NORMAL' ),
            'fresnel' : O( 'float', 'Fresnel' ),
            'facing' : O( 'float', 'Facing' ),
        }
    
    def get_function( self ):
        return 'layer_weight( blend, normal, fresnel, facing );\n'
    
NODES = [ MaltNodeLayerWeight ]