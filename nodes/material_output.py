from .utils import *

# CURRENTLY NOT SUPPORTED BY MALT

class MaltNodeMaterialOutput( EssentialsNode ):
    bl_idname = 'MaltNodeMaterialOutput'
    bl_label = 'Material Output'
    menu_category = 'OUTPUT'

    def define_sockets( self ):
        return{
            'color' : I( 'vec4', 'Color', subtype = 'Color', default = ( 0.5, 0.5, 0.5, 1 )),
            'line_color' : I( 'vec4', 'Line Color', subtype = 'Color', default = ( 0.0, 0.0, 0.0 )),
            'width_scale' : I( 'float', 'Line Width', default = 0.3 ),
            'normal_width' : I( 'float', 'Normal Line Width', default = 0.8 )
        }
    
    def get_fucntion( self ):
        f = '#ifdef MAIN_PASS\n'
        f += 'OUT_MAIN_PASS_PIXEL_SHADER_COLOR = color;\n'
        f += 'OUT_MAIN_PASS_PIXEL_SHADER_LINECOLOR = line_color;\n'
        f += 'OUT_MAIN_PASS_PIXEL_SHADER_LINEWIDTH = line_width( width_scale, vec4(1), 1, -0.3, 0.5, 1, normal_width, -0.4, 0.9, 0.2 );\n'
        f += '#endif //MAIN_PASS'
    
NODES = [ ]