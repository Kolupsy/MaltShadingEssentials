from bpy.props import *
from .utils import *

dimensions_items = [
    ( 'VEC2', '2', 'Vec2' ),
    ( 'VEC3', '3', 'Vec3' ),
    ( 'VEC4', '4', 'Vec4' ),
    ( 'VEC4C', '4C', 'Vec4 Color')
]

visible_socket = {
    'VEC2':'uv',
    'VEC3':'vector',
    'VEC4':'color',
    'VEC4C':'color'
}

class CombineSeparateXYZ( EssentialsNode ):
    menu_category = 'CONVERTOR'
    default_width = 145

    dimension : EnumProperty( name = 'Dimension', items = dimensions_items, default = 'VEC4', update = socket_update )

    def update_socket_visibility( self ):
        visible_socket_name = visible_socket[ self.dimension ]
        for i in self.inputs:
            i.enabled = i.name == visible_socket_name
        self.outputs['x'].enabled = self.dimension != 'VEC4C'
        self.outputs['y'].enabled = self.dimension != 'VEC4C'
        self.outputs['z'].enabled = self.dimension in [ 'VEC3', 'VEC4' ]
        self.outputs['w'].enabled = self.dimension in [ 'VEC4', 'VEC4C']
        self.outputs['split_color'].enabled = self.dimension == 'VEC4C'
        self.update_tree( )

    def define_sockets( self ):
        return{
            'uv' : I( 'vec2', 'UV', default = 'vec2( 0.0 )' ),
            'vector' : I( 'vec3', 'Vector', default = 'vec3( 0.0 )' ),
            'color' : I( 'vec4', 'Color', subtype = 'Color' ),
            'split_color' : O( 'vec3', 'Color 3', subtype = 'Color' ),
            'x' : O( 'float', 'X' ),
            'y' : O( 'float', 'Y' ),
            'z' : O( 'float', 'Z' ),
            'w' : O( 'float', 'W' )
        }
    
    def get_function( self ):
        return {
            'VEC2' : 'x = uv.x;     y = uv.y;',
            'VEC3' : 'x = vector.x; y = vector.y;   z = vector.z;',
            'VEC4' : 'x = color.x;  y = color.y;    z = color.z;      w = color.w;',
            'VEC4C': 'split_color = color.xyz;                        w = color.w;'
        }[ self.dimension ]
    
    def draw_buttons( self, context, layout ):
        layout.prop_tabs_enum( self, 'dimension' )

class MaltNodeSeparate( CombineSeparateXYZ ):
    bl_idname = 'MaltNodeSeparate'
    bl_label = 'Separate'

class MaltNodeCombine( CombineSeparateXYZ ):
    bl_idname = 'MaltNodeCombine'
    bl_label = 'Combine'

    def update_socket_visibility(self):
        visible_socket_name = visible_socket[ self.dimension ]
        for o in self.outputs:
            o.enabled = o.name == visible_socket_name
        self.inputs['x'].enabled = self.dimension != 'VEC4C'
        self.inputs['y'].enabled = self.dimension != 'VEC4C'
        self.inputs['z'].enabled = self.dimension in [ 'VEC3', 'VEC4' ]
        self.inputs['w'].enabled = self.dimension in ['VEC4', 'VEC4C' ]
        self.inputs['split_color'].enabled = self.dimension == 'VEC4C'
        self.update_tree( )
    
    def define_sockets( self ):
        return{
            'split_color' : I('vec3', 'Color 3', subtype = 'Color' ),
            'x' : I( 'float', 'X' ),
            'y' : I( 'float', 'Y' ),
            'z' : I( 'float', 'Z' ),
            'w' : I( 'float', 'W' ),
            'uv' : O( 'vec2', 'UV' ),
            'vector' : O( 'vec3', 'Vector' ),
            'color' : O( 'vec4', 'Color' )
        }
    def get_function( self ):
        return {
            'VEC2' : 'uv        = vec2( x, y );',
            'VEC3' : 'vector    = vec3( x, y, z );',
            'VEC4' : 'color     = vec4( x, y, z, w );',
            'VEC4C': 'color     = vec4( split_color, w );'
        }[ self.dimension ]

class MaltNodeSeparateHSV( EssentialsNode ):
    bl_idname = 'MaltNodeSeparateHSV'
    bl_label = 'Separate HSV'
    menu_category = 'CONVERTOR'

    def define_sockets( self ):
        return{
            'color' : I( 'vec3', 'Color', default = 'vec3( 0.8, 0.8, 0.8 )'),
            'h' : O( 'float', 'H' ),
            's' : O( 'float', 'S' ),
            'v' : O( 'float', 'V' ),
        }
    
    def get_function( self ):
        return '''
        vec3 hsv = rgb_to_hsv( color );
        h = hsv.x;
        s = hsv.y;
        v = hsv.z;
        '''

class MaltNodeCombineHSV( EssentialsNode ):
    bl_idname = 'MaltNodeCombineHSV'
    bl_label = 'Combine HSV'
    menu_category = 'CONVERTOR'

    def define_sockets( self ):
        return{
            'h' : I( 'float', 'H', default = 0.5 ),
            's' : I( 'float', 'S', default = 1.0 ),
            'v' : I( 'float', 'V', default = 1.0 ),
            'color' : O( 'vec3', 'Color' ),
        }
    
    def get_function( self ):
        return'color = hsv_to_rgb(vec3( h, s, v ));'
    
NODES = [ MaltNodeSeparate, MaltNodeCombine, MaltNodeSeparateHSV, MaltNodeCombineHSV ]