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
        t = self.tangent_type
        self.inputs[ 'uv' ].enabled = t == 'UV_TANGENT'
        self.inputs[ 'offset' ].enabled = t == 'RADIAL'
        self.inputs[ 'rotation' ].enabled = t == 'RADIAL'

    def define_sockets( self ):
        return{
            'uv' : I( 'vec2', 'UV', default = 'UV[0]' ),
            'offset' : I( 'vec3', 'Offset', subtype = 'Vector' ),
            'rotation' : I( 'vec3', 'Rotation', subtype = 'Vector' ),
            'tangent' : O( 'vec3', 'Tangent' ),
        }
    
    def get_function( self ):
        return{
            'PRECOMP' : 'tangent = TANGENT;',
            'UV_TANGENT' : 'tangent = tangent_uv_tangent( uv );',
            'RADIAL' : 'tangent = tangent_radial( offset, rotation );',
        }[ self.tangent_type ]
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'tangent_type', text = '' )

NODES = [ MaltNodeTangent ]