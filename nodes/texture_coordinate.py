from bpy.props import *
from .utils import *

class MaltNodeTextureCoordinate( EssentialsNode ):
    bl_idname = 'MaltNodeTextureCoordinate'
    bl_label = 'Texture Coordinate'
    menu_category = 'INPUT'
    default_width = 150

    def define_sockets( self ):
        return{
            'uv_index' : I( 'int', 'UV Index', min = 0, default = 0 ),
            'generated' : O( 'vec3', 'Generated' ),
            'normal' : O( 'vec3', 'Object Normal' ),
            'uv' : O( 'vec2', 'UV' ),
            'object' : O( 'vec3', 'Object' ),
            'camera' : O( 'vec3', 'Camera' ),
            'window' : O( 'vec2', 'Window' ),
            'reflection' : O( 'vec3', 'Reflection' ), 
        }
    
    def get_function( self ):
        f = 'texture_coordinates( uv_index, generated, normal, uv, object, camera, window, reflection );\n'
        if self.id_data.graph_type == 'Screen':
            f += 'generated = view_direction( );'
        return f

class MaltNodeUVMap( EssentialsNode ):
    bl_idname = 'MaltNodeUVMap'
    bl_label = 'UV Map'
    menu_category = 'INPUT'
    default_width = 180

    def define_sockets( self ):
        return{
            'index' : I( 'int', 'Index', default = 0 ),
            'uv' : O( 'vec2', 'UV' ),
        }
    
    def get_function( self ):
        return 'uv = surface_uv( index );'

class MaltNodeSkyCoords( EssentialsNode ):
    bl_idname = 'MaltNodeSkyCoords'
    bl_label = 'Sky Coordinates'
    menu_category = 'INPUT'

    def define_sockets( self ):
        return{
            'horizon' : I( 'float', 'Horizon', default = 0.01 ),
            'vector' : O( 'vec3', 'Coordinates' )
        }
    
    def get_function( self ):
        return 'vector = sky_coords( view_direction( ), horizon );'

NODES = [ MaltNodeTextureCoordinate, MaltNodeUVMap, MaltNodeSkyCoords ]