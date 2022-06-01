from bpy.props import *
from .utils import *

mixrgb_rna = bpy.types.ShaderNodeMixRGB.bl_rna
blend_type_items = enum_from_rna( mixrgb_rna, 'blend_type' )


functions = {
    'MIX' : 'mix_blend',
    'ADD' : 'mix_add',
    'MULTIPLY' : 'mix_multiply',
    'SUBTRACT' : 'mix_subtract',
    'SCREEN' : 'mix_screen',
    'DIVIDE' : 'mix_divide',
    'DIFFERENCE' : 'mix_difference',
    'DARKEN' : 'mix_darken',
    'LIGHTEN' : 'mix_lighten',
    'OVERLAY' : 'mix_overlay',
    'DODGE' : 'mix_dodge',
    'BURN' : 'mix_burn',
    'HUE' : 'mix_hue',
    'SATURATION' : 'mix_saturation',
    'VALUE' : 'mix_value',
    'COLOR' : 'mix_color',
    'SOFT_LIGHT' : 'mix_soft_light',
    'LINEAR_LIGHT' : 'mix_linear_light',
    'CLAMP' : 'mix_clamp_color'
}

class MaltNodeMixRGB( EssentialsNode ):
    bl_idname = 'MaltNodeMixRGB'
    bl_label = 'Mix'
    menu_category = 'COLOR'

    blend_type : EnumProperty( items = blend_type_items, name = 'Blend Type', default = 'MIX', update = malt_update )
    clamp : BoolProperty( name = 'Clamp', default = False, update = malt_update )

    def define_sockets( self ) -> dict:
        return {
            'fac': I( 'float', 'Fac', min = 0.0, max = 1.0, default = 0.5, subtype = 'Factor' ),
            'col1': I( 'vec4', 'Color1', subtype = 'Color' ),
            'col2': I( 'vec4', 'Color2', subtype = 'Color' ),
            'result': O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        func_name = functions[ self.blend_type ]
        f = f'{func_name}( fac, col1, col2, result );\n'
        if self.clamp:
            f += 'result = clamp( result, vec4(0), vec4(1));'
        return f
    
    def draw_buttons( self, context, layout ):
        layout.prop( self, 'blend_type', text = '' )
        layout.prop( self, 'clamp', text = 'Clamp' )
    
    def draw_label( self ) -> str:
        return next( x[1] for x in blend_type_items if self.blend_type == x[0])

NODES = [ MaltNodeMixRGB ]