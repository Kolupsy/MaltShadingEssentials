from .utils import *
from bpy.props import *

tangent_type_items = [
    ( 'PRECOMP', 'Precomputed', 'Use precomputed tangents. Check "use precomputed tangents" in the mesh settings to use them.' ),
    ( 'UV_TANGENT', 'UV Tangents', 'Compute tangents from a UV input.' ),
    ( 'RADIAL', 'Radial', 'Tagents as outward-vectors from a common normal vector' ),
]

class MaltNodeTangent( EssentialsNode ):
    bl_idname = 'MaltNodeTangent'
    bl_label = 'Tangent'
    menu_category = 'INPUT'

    tangent_type : EnumProperty( name = 'Tangent Type', items = tangent_type_items, update = lambda s,c:s.update_config( ))

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def update_socket_visibility( self ):
        self.inputs[ 'uv' ].enabled = self.tangent_type == 'UV_TANGENT'
        self.inputs[ 'vector' ].enabled = self.tangent_type == 'RADIAL'

    def define_sockets( self ):
        return{
            'uv' : I( 'vec2', 'UV', default = 'UV[0]' ),
            'vector' : I( 'vec3', 'Vector', default = ( 0.0, 0.0, 1.0 )),
            'tangent' : O( 'vec3', 'Tangent' ),
        }
    
    def get_function( self ):
        f = 'precomp = TANGENT.xyz;\n'
        f += 'uv_based = compute_tangent( uv ).xyz;\n'
        return f

NODES = [ MaltNodeTangent ]