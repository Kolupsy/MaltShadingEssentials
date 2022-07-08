import bpy
from bpy.types import Operator
from bpy.props import IntProperty

class NodeOperator( Operator ):

    bl_options = {'UNDO'}
    palette_optional = False

    @classmethod
    def poll(cls, context ):
        try:
            if cls.palette_optional:
                return context.active_node.bl_rna.properties['palette'].fixed_type.identifier == 'Palette'
            else:
                return context.active_node.palette != None
        except:
            pass    

class MALTSE_OT_new_palette( NodeOperator ):
    bl_idname = 'maltse.new_palette'
    bl_label = 'New Palette'
    bl_description = 'Add a new palette to the active node'
    palette_optional = True

    def execute( self, context ):
        palette = bpy.data.palettes.new( 'MaltSE Palette' )
        for c in [
                    ( 0.275, 0.306, 0.404 ),
                    ( 0.188, 0.6, 0.459 ),
                    ( 0.345, 0.702, 0.408 ),
                    ( 0.855, 0.847, 0.451 ),
                    ( 0.937, 0.933, 0.706 ),
                    ( 1, 1, 1 ),
                    ( 0, 0, 0 )]:

            color = palette.colors.new( )
            color.color = c
        
        context.active_node.palette = palette
        return{'FINISHED'}

class MALTSE_OT_new_palette_color( NodeOperator ):
    bl_idname = 'maltse.new_palette_color'
    bl_label = 'New Color'
    bl_description = 'Add a new color to the active color palette'

    def execute( self, context ):
        context.active_node.palette.colors.new( )
        return{'FINISHED'}
    
class MALTSE_OT_remove_palette_color( NodeOperator ):
    bl_idname = 'maltse.remove_palette_color'
    bl_label = 'Remove Color'
    bl_description = 'Remove the color of given index from the palette'

    index : IntProperty( )

    def execute( self, context ):
        palette: bpy.types.Palette = context.active_node.palette
        palette.colors.remove( palette.colors[ self.index ])
        return{'FINISHED'}

CLASSES = [
    MALTSE_OT_new_palette,
    MALTSE_OT_new_palette_color,
    MALTSE_OT_remove_palette_color,
]