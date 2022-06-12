from .utils import *

class MaltNodeObjectInfo( EssentialsNode ):
    bl_idname = 'MaltNodeObjectInfo'
    bl_label = 'Object Info'
    menu_category = 'INPUT'

    def define_sockets( self ):
        return{
            'location' : O( 'vec3', 'Location' ),
            'matrix' : O( 'mat4', 'Object Matrix' ),
            'distance' : O( 'float', 'Distance' ),
            'id' : O( 'vec4', 'ID' ),
            'random' : O( 'vec4', 'Random' ),
        }
    
    def get_function( self ):
        f = 'object_info( location, matrix, distance, id, random );'
        return f

NODES = [ MaltNodeObjectInfo ]