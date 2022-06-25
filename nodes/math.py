from bpy.props import *
from .utils import *

mathnode_rna = bpy.types.ShaderNodeMath.bl_rna
math_op_items = enum_from_rna( mathnode_rna, 'operation' )

functions = {
    'ADD' : ( 'math_add', 2 ),
    'SUBTRACT' : ( 'math_subtract', 2 ),
    'MULTIPLY' : ( 'math_multiply', 2 ),
    'DIVIDE' : ( 'math_divide', 2 ),
    'POWER' : ( 'math_power', 2 ),
    'LOGARITHM' : ( 'math_logarithm', 2 ),
    'SQRT' : ( 'math_sqrt', 1 ),
    'INVERSE_SQRT' : ( 'math_inverse_sqrt', 1 ),
    'ABSOLUTE' : ( 'math_absolute', 1 ),
    'RADIANS' : ( 'math_radians', 1 ),
    'DEGREES' : ( 'math_degrees', 1 ),
    'MINIMUM' : ( 'math_minimum', 2 ),
    'MAXIMUM' : ( 'math_maximum', 2 ),
    'LESS_THAN' : ( 'math_less_than', 2 ),
    'GREATER_THAN' : ( 'math_greater_than', 2 ),
    'ROUND' : ( 'math_round', 1 ),
    'FLOOR' : ( 'math_floor', 1 ),
    'CEIL' : ( 'math_ceil', 1 ),
    'FRACT' : ( 'math_fraction', 1 ),
    'MODULO' : ( 'math_modulo', 2 ),
    'TRUNC' : ( 'math_trunc', 1 ),
    'SNAP' : ( 'math_snap', 2 ),
    'PINGPONG' : ( 'math_pingpong', 2 ),
    'WRAP' : ( 'math_wrap', 3 ),
    'SINE' : ( 'math_sine', 1 ),
    'COSINE' : ( 'math_cosine', 1 ),
    'TANGENT' : ( 'math_tangent', 1 ),
    'SINH' : ( 'math_sinh', 1 ),
    'COSH' : ( 'math_cosh', 1 ),
    'TANH' : ( 'math_tanh', 1 ),
    'ARCSINE' : ( 'math_arcsine', 1 ),
    'ARCCOSINE' : ( 'math_arccosine', 1 ),
    'ARCTANGENT' : ( 'math_arctangent', 1 ),
    'ARCTAN2' : ( 'math_arctan2', 2 ),
    'SIGN' : ( 'math_sign', 1 ),
    'EXPONENT' : ( 'math_exponent', 1 ),
    'COMPARE' : ( 'math_compare', 3 ),
    'MULTIPLY_ADD' : ( 'math_multiply_add', 3 ),
    'SMOOTH_MIN' : ( 'math_smoothmin', 3 ),
    'SMOOTH_MAX' : ( 'math_smoothmax', 3 )
}

class MaltNodeMath( EssentialsNode ):
    bl_idname = 'MaltNodeMath'
    bl_label = 'Math'
    menu_category = 'CONVERTOR'
    default_width = 160

    operation : EnumProperty( name = 'Operation', items = math_op_items, update = lambda s,c:s.update_operation( ))
    clamp : BoolProperty( name = 'Clamp', default = False, update = malt_update )

    @property
    def function_data( self ):
        return functions[ self.operation ]
    
    def update_operation( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def update_socket_visibility( self ):
        self.inputs[1].enabled = self.function_data[1] > 1
        self.inputs[2].enabled = self.function_data[1] > 2
    
    def define_sockets( self ):
        return{
            'a' : I( 'float', 'Value 1', default = 0.5 ),
            'b' : I( 'float', 'Value 2', default = 0.5 ),
            'c' : I( 'float', 'Value 3', default = 0.5 ),
            'result' : O( 'float', 'Value' ),
        }
    
    def get_function( self ):
        f = f'{self.function_data[0]}( a, b, c, result );\n'
        if self.clamp:
            f += 'result = clamp( result, 0.0, 1.0 );\n'
        return f
    
    def draw_buttons( self, context, layout ):
        c = layout.column( align = True )
        c.prop( self, 'operation', text = '' )
        c.prop( self, 'clamp' )
    
    def draw_label(self) -> str:
        return next( x[1] for x in math_op_items if self.operation == x[0] )

NODES = [ MaltNodeMath ]