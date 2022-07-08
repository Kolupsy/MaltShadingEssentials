from .utils import *
from bpy.props import BoolProperty, EnumProperty

filter_size_items = [
    ( '2', '2', '2x2 Matrix' ),
    ( '3', '3', '3x3 Matrix' ),
    ( '4', '4', '4x4 Matrix' ),
    ( '8', '8', '8x8 Matrix' ),
]

class MaltNodeBayerDither( EssentialsNode ):
    bl_idname = 'MaltNodeBayerDither'
    bl_label = 'Bayer Dither'
    menu_category = 'CONVERTOR'

    use_auto_screen : BoolProperty( name = 'Use Auto Screen', default = False, update = lambda s,c:s.update_config( ))
    filter_size : EnumProperty( name = 'Filter Size', items = filter_size_items, update = malt_update )

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def update_socket_visibility( self ):
        self.inputs['uv'].enabled = not self.use_auto_screen

    def define_sockets( self ):
        return{
            'uv' : I( 'vec2', 'UV', default = 'vec2( 0.0 )' ),
            'threshold' : O( 'float', 'Threshold' ),
        }
    
    def get_function( self ):
        
        f = ''
        if self.use_auto_screen:
            f += 'uv = fract(screen_uv( ) * ( render_resolution( ) / vec2( {num} )));\n'.format(
                num = {
                    '2' : '2.0',
                    '3' : '3.0',
                    '4' : '4.0',
                    '8' : '8.0',
                }[self.filter_size]
            )

        func = {
            '2' : 'bayer_dithering2',
            '3' : 'bayer_dithering3',
            '4' : 'bayer_dithering4',
            '8' : 'bayer_dithering8',
        }[ self.filter_size ]
        f += f'threshold = {func}( uv );\n'
        return f
    
    def draw_buttons( self, context, layout ):
        layout.prop_tabs_enum( self, 'filter_size' )
        layout.prop( self, 'use_auto_screen' )

NODES = [ MaltNodeBayerDither ]