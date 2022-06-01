from bpy.props import *
from .utils import *

dimensions_items = [
    ( '1D', '1D', '1-dimensional noise' ),
    ( '2D', '2D', '2-dimensional noise' ),
    ( '3D', '3D', '3-dimensional noise' ),
    ( '4D', '4D', '4-dimensional noise' )
]

socket_visibility = {
    '1D' : 'fac',
    '2D' : 'uv',
    '3D' : 'vector',
    '4D' : 'color'
}

class MaltNodeTexNoise( EssentialsNode ):
    bl_idname = 'MaltNodeTextNoise'
    bl_label = 'Noise Texture'
    menu_category = 'TEXTURE'
    default_width = 150

    dimensions : EnumProperty( name = 'Dimensions', items = dimensions_items, default = '2D', update = lambda s, c: s.update_dimensions( ))

    def update_dimensions( self ):
        self.update_socket_visibility( )
        self.update_tree( )

    def update_socket_visibility( self ):
        visible_socket_name = socket_visibility[ self.dimensions ]
        print( 'update socket vis', visible_socket_name )
        for i in [ x for x in self.inputs if x.name in socket_visibility.values( )]:
            i.enabled = i.name == visible_socket_name
    
    def define_sockets( self ):
        return{
            'fac' : I( 'float', 'Fac', default = 'float( 0.0 )' ),
            'uv' : I( 'vec2', 'UV', default = 'surface_uv( 0 )' ),
            'vector' : I( 'vec3', 'Vector', default = 'object_coords( )' ),
            'color' : I( 'vec4', 'Color', default = 'vec4( POSITION, 1.0 )' ),

            'scale': I( 'float', 'Scale', default = 5.0 ),
            'detail' : I( 'float', 'Detail', min = 0.0, max = 16.0, default = 1.0 ),
            'roughness' : I( 'float', 'Rough', min = 0.0, max = 1.0, default = 0.5 ),

            'value' : O( 'float', 'Value' ),
            'result' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        func_data = {
            '1D' : ( 'noise_texture1D', 'fac' ),
            '2D' : ( 'noise_texture2D', 'uv' ),
            '3D' : ( 'noise_texture3D', 'vector' ),
            '4D' : ( 'noise_texture4D', 'color' ),
        }[ self.dimensions ]
        print( func_data )
        return f'{func_data[0]}( {func_data[1]}, scale, detail, roughness, value, result );'
    
    def draw_buttons(self, context, layout ):
        layout.prop( self, 'dimensions', text = '' )

NODES = [ MaltNodeTexNoise ]