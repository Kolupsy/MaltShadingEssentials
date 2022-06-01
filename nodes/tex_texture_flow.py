from .utils import *

class MaltNodeTextureFlow( EssentialsNode ):
    bl_idname = 'MaltNodeTextureFlow'
    bl_label = 'Texture Flow'
    menu_category = 'TEXTURE'
    default_width = 250

    def define_sockets( self ):
        return{
            'image' : I( 'sampler2D', 'Image' ),
            'uv' : I( 'vec2', 'UV', default = 'UV[0]' ),
            'flow' : I( 'vec2', 'Flow', default = 'vec2(0.0)' ),
            'time' : I( 'float', 'Time' ),
            'samples' : I( 'int', 'Samples', min = 2, default = 2 ),
            'color' : O( 'vec4', 'Color' ),
        }
    
    def get_function( self ):
        return 'color = texture_flow( image, uv, flow, time, samples );'

NODES = [ MaltNodeTextureFlow ]