from .utils import *

class MaltNodeObjectInfo( EssentialsNode ):
    bl_idname = 'MaltNodeObjectInfo'
    bl_label = 'Object Info'
    menu_category = 'INPUT'
    default_width = 140

    def define_sockets( self ):
        return{
            'location' : O( 'vec3', 'Location' ),
            'rotation' : O( 'vec3', 'Rotation (TODO)' ),
            'scale' : O( 'vec3', 'Scale' ),
            'matrix' : O( 'mat4', 'Object Matrix' ),
            'distance' : O( 'float', 'Distance' ),
            'id' : O( 'vec4', 'Name ID' ),
            'random' : O( 'vec4', 'Random' ),
        }
    
    def get_function( self ):
        f = 'object_info( location, scale, matrix, distance, id, random );'
        return f

NODES = [ MaltNodeObjectInfo ]