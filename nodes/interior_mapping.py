from .utils import *

class MaltNodeInteriorMapping( EssentialsNode ):
    bl_idname = 'MaltNodeInteriorMapping'
    bl_label = 'Interior Mapping'
    menu_category = 'INPUT'
    default_width = 180

    def define_sockets( self ):
        return{
            'position' : I( 'vec3', 'Position', subtype = 'Vector', default = 'POSITION' ),
            'incoming' : I( 'vec3', 'Incoming', subtype = 'Vector', default = 'incoming_vector( )'),
            'room_dimensions' : I( 'vec3', 'Dimensions', subtype = 'Vector', default = ( 1.0, 1.0 , 1.0 )),
            'mapping' : O( 'vec3', 'Mapping' ),
            'wall_masks' : O( 'vec4', 'Wall Masks' ),
            'wall_index' : O( 'float', 'Wall Index' ),
        }
    
    def get_function( self ):
        return 'interior_mapping( position, incoming, room_dimensions, mapping, wall_masks, wall_index );\n'
    
NODES = [ MaltNodeInteriorMapping ]