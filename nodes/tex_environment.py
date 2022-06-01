from .utils import *
from bpy.props import *

class MaltNodeTexEnvironment( EssentialsNode ):
    bl_idname = 'MaltNodeTexEnvironment'
    bl_label = 'Environment Texture'
    menu_category = 'TEXTURE'

    def define_sockets( self ):
        return{
            'image' : I( 'sampler2D', 'Image' ),
            'vector' : I( 'vec3', 'Vector', subtype = 'Vector', default = 'POSITION' ),
            'color' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        return 'color = sampler2D_sample_environment( image, vector );'
    
NODES = [ MaltNodeTexEnvironment ]