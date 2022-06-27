from .utils import *

class MaltNodeTexHexTiles( EssentialsNode ):
    bl_idname = 'MaltNodeTexHexTiles'
    bl_label = 'Hexagon Tiles'
    menu_category = 'TEXTURE'
    default_width = 155

    def define_sockets( self ):
        return{
            'uv' : I( 'vec2', 'UV', default = 'UV[0]' ),
            'scale' : I( 'float', 'Scale', default = 5.0 ),
            'tile_size' : I( 'float', 'Tile Size', default = 0.9, min = 0.0, max = 1.0 ),
            'tile_uv' : O( 'vec2', 'UV' ),
            'tile_pos' : O( 'vec2', 'Position' ),
            'tile_mask' : O( 'float', 'Mask' ),
            'tile_gradient' : O( 'float', 'Gradient' ),
            'random_id' : O( 'vec4', 'Random' )
        }
    
    def get_function( self ):
        return 'hexagon_tiles( uv, scale, tile_size, tile_uv, tile_pos, tile_mask, tile_gradient, random_id );\n'

NODES = [ MaltNodeTexHexTiles ]