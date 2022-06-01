from bpy.props import *
from .utils import *

maprange_rna = bpy.types.ShaderNodeMapRange.bl_rna
interpolation_type_items = enum_from_rna( maprange_rna, 'interpolation_type' )

class MaltNodeMapRange( EssentialsNode ):
    bl_idname = 'MaltNodeMapRange'
    bl_label = 'Map Range'
    menu_category = 'CONVERTOR'

    clamp : BoolProperty( name = 'Clamp', default = False, update = malt_update )
    interpolation_type : EnumProperty( name = 'Interpolation Type', items = interpolation_type_items, update = lambda s,c: s.update_interpolation( ))

    def update_socket_visibility( self ):
        self.inputs[ 'steps' ].enabled = self.interpolation_type == 'STEPPED'
    
    def update_interpolation( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def define_sockets( self ):
        return{
            'value' : I( 'float', 'Value', default = 0.5 ),
            'from_min' : I( 'float', 'From Min', default = 0.0 ),
            'from_max' : I( 'float', 'From Max', default = 1.0 ),
            'to_min' : I( 'float', 'To Min', default = 0.0 ),
            'to_max' : I( 'float', 'To Max', default = 1.0 ),
            'steps' : I( 'int', 'Steps', default = 4 ),
            'result' : O( 'float', 'Result' )
        }
    
    def get_function( self ):
        func = {
            'LINEAR': 'float_map_range_linear',
            'STEPPED': 'float_map_range_stepped',
            'SMOOTHSTEP': 'float_map_range_smoothstep',
            'SMOOTHERSTEP': 'float_map_range_smootherstep'
        }[ self.interpolation_type ]
        f = f'{func}( value, from_min, from_max, to_min, to_max, steps, result );\n'
        if self.clamp:
            f += 'result = clamp( result, min( to_min, to_max ), max( to_max, to_min ));\n'
        return f
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'interpolation_type', text = '' )
        layout.prop( self, 'clamp' )

NODES = [ MaltNodeMapRange ]