from bpy.props import *
from .utils import *

class ImageNode( EssentialsNode ):
    menu_category = 'TEXTURE'
    default_width = 320

    sample_closest : BoolProperty( name = 'Sample Closest', default = False, update = malt_update )
    
    def get_image( self ) -> bpy.types.Image:
        return self.malt_parameters.textures['image'].texture
    def set_image( self, image:bpy.types.Image ):
        self.malt_parameters.textures['image'].texture = image

    def define_sockets( self ):
        return{
            'image' : I( 'sampler2D', 'Image' ),
            'uv' : I( 'vec2', 'UV', default = 'surface_uv( 0 )' ),
            'color' : O( 'vec4', 'Color' ),
        }
    
    def get_function( self ):
        func_name = 'sampler2D_sample'
        if self.sample_closest:
            func_name += '_nearest'
        return f'color = {func_name}( image, uv );\n'

    def draw_socket( self, context, layout, socket, text ):
        super( ).draw_socket( context, layout, socket, text )
        if socket.name == 'uv':
            layout.prop( self, 'sample_closest', toggle = 1 )

class MaltNodeTexImage( ImageNode ):
    bl_idname = 'MaltNodeTexImage'
    bl_label = 'Image Texture'

class MaltNodeNormalMap( ImageNode ):
    bl_idname = 'MaltNodeNormalMap'
    bl_label = 'Normal Map'

    def define_sockets( self ):
        return{
            'image' : I( 'sampler2D', 'Image' ),
            'uv' : I( 'vec2', 'UV', default = 'surface_uv( 0 )' ),
            'uv_index' : I( 'int', 'UV Index', default = 0 ),
            'color' : O( 'vec4', 'Normal' ),
        }

    def get_function( self ):
        f = super( ).get_function( )
        f += 'color.xyz = normalize( get_TBN( uv_index ) * ( color.xyz * 2.0 - 1.0 ));\n'
        return f
    
    def draw_buttons( self, context, layout ):
        layout = layout.column( )
        layout.scale_y = 0.3
        if image := self.malt_parameters.textures['image'].texture:
            if not image.colorspace_settings.name in [ 'Non-Color', 'Linear' ]:
                layout.label( text = 'Color Management Alert', icon = 'ERROR' )

NODES = [ MaltNodeTexImage, MaltNodeNormalMap ] 