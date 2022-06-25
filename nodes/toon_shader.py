from .utils import *
from bpy.props import *

class MaltNodeToonShader( EssentialsNode ):
    bl_idname = 'MaltNodeToonShader'
    bl_label = 'Toon Shader'
    menu_category = 'SHADER'
    default_width = 190

    def define_sockets( self ):
        return{
            'size' : I( 'float', 'Size', default = 0.5, min = 0.0 ),
            'gradient_size' : I( 'float', 'Gradient', default = 0.0, min = 0.0, max = 1.0 ),
            'specular' : I( 'float', 'Specular', default = 0.0, min = 0.0, max = 1.0 ),
            'offset' : I( 'float', 'Offset', default = 0.0 ),
            'position' : I( 'vec3', 'Position', default = 'POSITION' ),
            'normal' : I( 'vec3', 'Normal', default = 'NORMAL' ),
            'group' : I( 'int', 'Group', default = 1 ),
            'shadows' : I( 'bool', 'Shadows', default = True ),
            'self_shadows' : I( 'bool', 'Self Shadows', default = True ),
            'result' : O( 'vec3', 'Color' ),
            'line_mask' : O( 'float', 'Line Mask' ),
        }
    
    def get_function( self ):
        f = 'result = toon_shading( position, normal, size, gradient_size, clamp( specular, 0.0, 1.0 ), offset, group, shadows, self_shadows );\n'
        f += 'line_mask = float_from_vec3( result );'
        return f
    
NODES = [ MaltNodeToonShader ]