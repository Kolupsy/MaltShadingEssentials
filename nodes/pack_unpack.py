from .utils import *

class MaltNodePack( EssentialsNode ):
    bl_idname = 'MaltNodePack'
    bl_label = 'Pack'
    menu_category = 'CONVERTOR'
    default_width = 140

    def define_sockets( self ):
        return{
            'color1' : I( 'vec4', 'Color 1' ),
            'color2' : I( 'vec4', 'Color 2' ),
            'color3' : I( 'vec4', 'Color 3' ),
            'color4' : I( 'vec4', 'Color 4' ),
            'result' : O( 'uvec4', 'Packed' )
        }
    
    def get_function( self ):
        return 'result = pack_8bit( color1, color2, color3, color4 );\n'

class MaltNodeUnpack( EssentialsNode ):
    bl_idname = 'MaltNodeUnpack'
    bl_label = 'Unpack'
    menu_category = 'CONVERTOR'
    default_width = 140

    def define_sockets( self ):
        return{
            'packed_data' : I( 'uvec4', 'Packed', default = 'uvec4( 0 )' ),
            'color1' : O( 'vec4', 'Color 1' ),
            'color2' : O( 'vec4', 'Color 2' ),
            'color3' : O( 'vec4', 'Color 3' ),
            'color4' : O( 'vec4', 'Color 4' ),
        }
    
    def get_function( self ):
        return 'unpack_8bit( packed_data, color1, color2, color3, color4 );\n'

NODES = [ MaltNodePack, MaltNodeUnpack ]