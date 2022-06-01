from bpy.props import *
from .utils import *

class MaltNodeColorRamp( EssentialsNode ):
    bl_idname = 'MaltNodeColorRamp'
    bl_label = 'Color Ramp'
    menu_category = 'CONVERTOR'

    show_ramp : BoolProperty( name = 'Expose', description = 'Toggle whether the color ramp should be exposed as an input', default = False, update = socket_update )

    def get_ramp_texture( self ) -> bpy.types.Texture:
        return self.malt_parameters.gradients['color_ramp'].texture
    def new_ramp_texture( self ):
        self.malt_parameters.gradients['color_ramp'].add_or_duplicate( )

    def on_init( self ):
        self.new_ramp_texture( )
    
    def copy( self, node:'MaltNodeColorRamp' ):
        self.new_ramp_texture( )
    
    def free( self ):
        texture = self.get_ramp_texture( )
        if not texture.use_fake_user and texture.users == 1:
            bpy.data.textures.remove( texture )
    
    def update_socket_visibility( self ):
        inp = self.inputs['color_ramp']
        if inp.is_linked and not self.show_ramp:
            link = inp.links[0]
            self.id_data.links.remove( link )
        inp.enabled = self.show_ramp
    
    def define_sockets( self ):
        return{
            'color_ramp' : I( 'sampler1D', 'Ramp' ),
            'fac' : I( 'float', 'Fac', min = 0.0, max = 1.0, default = 0.5 ),
            'color' : O( 'vec4', 'Color' ),
        }
    
    def get_function( self ):
        return 'color = sampler1D_sample( color_ramp, fac );\n'
    
    def draw_buttons( self, context, layout ):
        if not self.inputs['color_ramp'].is_linked and not self.show_ramp:
            layout.template_color_ramp( self.get_ramp_texture( ), 'color_ramp' )
    
    def draw_socket( self, context, layout, socket, text ):
        if socket.name == 'color':
            layout.prop( self, 'show_ramp', toggle = 1 )
        return super( ).draw_socket( context, layout, socket, text )

NODES = [ MaltNodeColorRamp ]