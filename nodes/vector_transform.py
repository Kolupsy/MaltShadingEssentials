from bpy.props import *
from .utils import *

transformnode_rna = bpy.types.ShaderNodeVectorTransform.bl_rna

vector_type_items = enum_from_rna( transformnode_rna, 'vector_type' )
convert_from_items = enum_from_rna( transformnode_rna, 'convert_from' )
convert_to_items = enum_from_rna( transformnode_rna, 'convert_to' )

class MaltNodeVectorTransform( EssentialsNode ):
    bl_idname = 'MaltNodeVectorTransform'
    bl_label = 'Vector Transform'
    menu_category = 'VECTOR'

    vector_type : EnumProperty( name = 'Vector Type', items = vector_type_items, update = malt_update )
    convert_from : EnumProperty( name = 'Convert From', default = 0, items = convert_from_items, update = malt_update )
    convert_to : EnumProperty( name = 'Convert To', default = 1, items = convert_to_items, update = malt_update )

    def define_sockets( self ):
        return{
            'vector' : I( 'vec3', 'Vector', default = 'vec3(0)' ),
            'result' : O( 'vec3', 'Vector' )
        }
    
    def get_function( self ):
        funcs = {
            'OBJECT_WORLD': 'result = transform_{type}( MODEL, vector );',
            'WORLD_OBJECT': 'result = transform_{type}( inverse( MODEL ), vector );',
            'WORLD_CAMERA': 'result = transform_{type}( CAMERA, vector );',
            'CAMERA_WORLD': 'result = transform_{type}( inverse( CAMERA ), vector );',
            'OBJECT_CAMERA': 'result = transform_{type}( CAMERA, transform_{type}( MODEL, vector ));',
            'CAMERA_OBJECT': 'result = transform_{type}( inverse( CAMERA ), transform_{type}( inverse( MODEL ), vector ));'
        }
        transform_type = {
            'POINT': 'point',
            'VECTOR': 'direction',
            'NORMAL': 'normal'
        }[ self.vector_type ]
        conversion = f'{ self.convert_from }_{ self.convert_to }'
        if conversion in funcs.keys( ):
            f = funcs[ conversion ].format( type = transform_type )
        else:
            f = 'result = vector;'
        f += '\n'
        return f
    
    def draw_buttons( self, context, layout ):

        layout.prop_tabs_enum( self, 'vector_type' )
        c = layout.column( align = True )
        c.prop( self, 'convert_from', text = '' )
        c.prop( self, 'convert_to', text = '' )
    
NODES = [ MaltNodeVectorTransform ]