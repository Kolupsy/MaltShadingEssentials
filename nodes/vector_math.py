from bpy.props import *
from .utils import *

vectormath_rna = bpy.types.ShaderNodeVectorMath.bl_rna
vectormath_op_items = enum_from_rna( vectormath_rna, 'operation' )

functions = {
    'ADD' : ( 'vector_math_add', 'Addend 1', 'Addend 2', '', '', 'Sum', '' ),
    'SUBTRACT' : ( 'vector_math_subtract', 'Minuend', 'Subtrahend', '', '', 'Difference', '' ),
    'MULTIPLY' : ( 'vector_math_multiply', 'Factor 1', 'Factor 2', '', '', 'Product', '' ),
    'DIVIDE' : ( 'vector_math_divide', 'Dividend', 'Divisor', '', '', 'Quotient', '' ),
    'CROSS_PRODUCT' : ( 'vector_math_cross', 'Vector 1', 'Vector 2', '', '', 'Cross', '' ),
    'PROJECT' : ( 'vector_math_project', 'Vector', 'Base', '', '', 'Projected', '' ),
    'REFLECT' : ( 'vector_math_reflect', 'Incoming', 'Normal', '', '', 'Reflected', '' ),
    'DOT_PRODUCT' : ( 'vector_math_dot', 'Vector 1', 'Vector 2', '', '', '', 'Dot' ),
    'DISTANCE' : ( 'vector_math_distance', 'Vector 1', 'Vector 2', '', '', '', 'Distance' ),
    'LENGTH' : ( 'vector_math_length', 'Vector', '', '', '', '', 'Length' ),
    'SCALE' : ( 'vector_math_scale', 'Vector', '', '', 'Scalar', 'Scaled', '' ),
    'NORMALIZE' : ( 'vector_math_normalize', 'Vector', '', '', '', 'Normalized', '' ),
    'SNAP' : ( 'vector_math_snap', 'Dividend', 'Divisor', '', '', 'Vector', '' ),
    'FLOOR' : ( 'vector_math_floor', 'Vector', '', '', '', 'Vector', '' ),
    'CEIL' : ( 'vector_math_ceil', 'Vector', '', '', '', 'Vector', '' ),
    'MODULO' : ( 'vector_math_modulo', 'Vector 1', 'Vector 2', '', '', 'Vector', '' ),
    'WRAP' : ( 'vector_math_wrap', 'Vector 1', 'Vector 2', 'Vector 3', '', 'Vector', '' ),
    'FRACTION' : ( 'vector_math_fraction', 'Vector', '', '', '', 'Fraction', '' ),
    'ABSOLUTE' : ( 'vector_math_absolute', 'Vector', '', '', '', 'Absolute', '' ),
    'MINIMUM' : ( 'vector_math_minimun', 'Vector 1', 'Vector 2', '', '', 'Minimum', '' ),
    'MAXIMUM' : ( 'vector_math_maximum', 'Vector 1', 'Vector 2', '', '', 'Maximum', '' ),
    'SINE' : ( 'vector_math_sine', 'Vector', '', '', '', 'Vector', '' ),
    'COSINE' : ( 'vector_math_cosine', 'Vector', '', '', '', 'Vector', '' ),
    'TANGENT' : ( 'vector_math_tangent', 'Vector', '', '', '', 'Vector', '' ),
    'REFRACT' : ( 'vector_math_refract', 'Incoming', 'Normal', '', 'IOR', 'Refracted', '' ),
    'FACEFORWARD' : ( 'vector_math_faceforward', 'Vector 1', 'Vector 2', 'Vector 3', '', 'Vector', '' ),
    'MULTIPLY_ADD' : ( 'vector_math_multiply_add', 'Factor 1', 'Factor 2', 'Addend', '', 'Vector', '' )
}

class MaltNodeVectorMath( EssentialsNode ):
    bl_idname = 'MaltNodeVectorMath'
    bl_label = 'Vector Math'
    menu_category = 'CONVERTOR'
    default_width = 180

    operation : EnumProperty( name = 'Operation', items = vectormath_op_items, update = lambda s,c: s.update_operation( ))

    @property
    def function_data( self ):
        return functions[ self.operation ]
    
    def update_operation( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def map_function_data_sockets( self ):
        return zip( list( self.function_data )[1:], list( self.inputs ) + list( self.outputs ))
    
    def update_socket_visibility( self ):
        for name, socket in self.map_function_data_sockets( ):
            socket.enabled = name != ''
    
    def define_sockets( self ):
        return {
            'a' : I( 'vec3', 'Vector 1', subtype = 'Vector' ),
            'b' : I( 'vec3', 'Vector 2', subtype = 'Vector' ),
            'c' : I( 'vec3', 'Vector 3', subtype = 'Vector' ),
            'scale' : I( 'float', 'Scale', default = 1.0 ),
            'outVector' : O( 'vec3', 'Vector' ),
            'outValue' : O( 'float', 'Value' )
        }
    
    def get_function( self ):
        return f'{self.function_data[0]}( a, b, c, scale, outVector, outValue );\n'
    
    def draw_socket_name( self, socket ):
        return next( name for name, socket_ in self.map_function_data_sockets( ) if socket_ == socket )
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'operation', text = '' )
    
    def draw_label( self ):
        return next( x[1] for x in vectormath_op_items if self.operation == x[0])

NODES = [ MaltNodeVectorMath ]