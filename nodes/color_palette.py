from .utils import *
from bpy.props import PointerProperty
from ..color_palette_ui import MALTSE_OT_new_palette, MALTSE_OT_new_palette_color, MALTSE_OT_remove_palette_color

class MaltNodeColorPalette( EssentialsNode ):
    bl_idname = 'MaltNodeColorPalette'
    bl_label = 'Color Palette'
    menu_category = 'COLOR'

    palette : PointerProperty( type = bpy.types.Palette, name = 'Palette', update = malt_update )

    def define_sockets( self ):
        return{
            'in_color' : I( 'vec4', 'Color', subtype = 'Color', default = ( 0.8, 0.8, 0.8, 1.0 )),
            'result' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        return f'result = color_paletting( in_color, {self.get_color_array( )} );'
    
    def get_color_array( self ) -> str:
        if not self.palette:
            colors = [(0.0, 0.0, 0.0 )]
        else:
            colors = [ x.color for x in self.palette.colors ]
        if not len( colors ):
            colors = [( 0.0, 0.0, 0.0 )]
        result = 'vec4[16]('
        for i in range( 16 ):
            c = colors[ min( i, len( colors ) - 1 )]
            result += f'vec4( {c[0]}, {c[1]}, {c[2]}, 1.0 ),'
        result = result[:-1]
        result += ')'
        return result
    
    def draw_buttons( self, context, layout ):
        self.override_context( layout )
        layout.template_ID( self, 'palette', text = '', new = MALTSE_OT_new_palette.bl_idname )
        if self.palette:
            c = layout.column( align = True )
            c.scale_y = 0.8
            self.override_context( c )
            for i, color in enumerate( self.palette.colors ):
                row = c.row( align = True )
                row.prop( color, 'color', text = '' )
                op = row.operator( MALTSE_OT_remove_palette_color.bl_idname, text = '', icon = 'REMOVE' )
                op.index = i
            c.operator( MALTSE_OT_new_palette_color.bl_idname, text = 'Add Color', icon = 'COLOR' )
    
    def draw_label( self ) -> str:
        if self.palette:
            return self.palette.name
        else:
            return self.bl_label

NODES = [ MaltNodeColorPalette ]