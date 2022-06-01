from .utils import *
from bpy.props import *

mapping_rna = bpy.types.ShaderNodeMapping.bl_rna

vector_type_items = enum_from_rna( mapping_rna, 'vector_type' )

class MaltNodeMapping( EssentialsNode ):
    bl_idname = 'MaltNodeMapping'
    bl_label = 'Mapping'
    menu_category = 'VECTOR'

    vector_type : EnumProperty( name = 'Vector Type', items = vector_type_items, update = lambda s,c:s.update_config( ))

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )

    def update_socket_visibility( self ):
        self.inputs[ 'location' ].enabled = self.vector_type in [ 'POINT', 'TEXTURE' ]

    def define_sockets( self ):
        return{
            'vector' : I( 'vec3', 'Vector', default = 'vec3(0.0)' ),
            'location' : I( 'vec3', 'Location', subtype = 'Vector' ),
            'rotation' : I( 'vec3', 'Rotation', subtype = 'Vector' ),
            'scale' : I( 'vec3', 'Scale', subtype = 'Vector', default = ( 1.0, 1.0, 1.0 )),
            'result' : O( 'vec3', 'Result' ),
        }
    
    def get_function( self ):
        return{
            'POINT' : 'result = vector_mapping_point( vector, location, rotation, scale );',
            'TEXTURE' : 'result = vector_mapping_texture( vector, location, rotation, scale );',
            'VECTOR' : 'result = vector_mapping_vector( vector, rotation, scale );',
            'NORMAL' : 'result = vector_mapping_normal( vector, rotation, scale );',
        }[ self.vector_type ]
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'vector_type', text = '' )

NODES = [ MaltNodeMapping ]