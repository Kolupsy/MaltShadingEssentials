from .utils import *
from bpy.props import *

transformation_type_items = [
    ( 'POINT', 'Point', 'Transform Point' ),
    ( 'VECTOR', 'Vector', 'Transform Vector' ),
    ( 'NORMAL', 'Normal', 'Transform Normal' ),
]

class MaltNodeMatrices( EssentialsNode ):
    bl_idname = 'MaltNodeMatrices'
    bl_label = 'Matrices'
    menu_category = 'INPUT'

    def define_sockets( self ):
        return{
            'model' : O( 'mat4', 'Object' ),
            'camera' : O( 'mat4', 'Camera' ),
            'projection' : O( 'mat4', 'Projection' )
        }
    
    def get_function( self ):
        return 'model = MODEL; camera = CAMERA; projection = PROJECTION;\n'

class MaltNodeTransformation( EssentialsNode ):
    bl_idname = 'MaltNodeTransformation'
    bl_label = 'Transformation'
    menu_category = 'VECTOR'

    transformation_type : EnumProperty( name = 'Transformation Type', items = transformation_type_items, update = malt_update )

    def define_sockets( self ):
        return{
            'matrix' : I( 'mat4', 'Matrix', default = 'mat4( 0.0 )' ),
            'vector' : I( 'vec3', 'Vector', subtype = 'Vector' ),
            'invert' : I( 'bool', 'Invert', default = False ),
            'result' : O( 'vec3', 'Vector' )
        }
    
    def get_function( self ):
        func_name = {
            'POINT' : 'transform_point',
            'VECTOR' : 'transform_direction',
            'NORMAL' : 'transform_normal',
        }[ self.transformation_type ]
        f = 'matrix = invert ? inverse( matrix ) : matrix;\n'
        f += f'result = {func_name}( matrix, vector );\n'
        return f
    
    def draw_buttons( self, context, layout ):
        layout.prop_tabs_enum( self, 'transformation_type' )

NODES = [ MaltNodeMatrices, MaltNodeTransformation ]