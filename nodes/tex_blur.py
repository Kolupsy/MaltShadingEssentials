from .utils import *
from bpy.props import *

blur_mode_items = [
    ( 'BOX', 'Box', 'Box Blur Mode' ),
    ( 'GAUSSIAN', 'Gaussian', 'Gaussian Blur Mode' ),
    ( 'JITTER', 'Jitter', 'Jitter Blur Mode / Noise Dithering' ),
]
calculation_mode_items = [
    ( 'ABSOLUTE', 'Absolute Radius', 'Calculate the blur using an absolute pixel radius number' ),
    ( 'RATIO', 'Ratio', 'Calculate the blur size relative to the texture size' ),
]

class MaltNodeTexBlur( EssentialsNode ):
    bl_idname = 'MaltNodeTexBlur'
    bl_label = 'Blur'
    menu_category = 'TEXTURE'
    default_width = 200

    blur_mode : EnumProperty( name = 'Blur Mode', items = blur_mode_items, update = lambda s,c:s.update_config( ))
    calculation_mode : EnumProperty( name = 'Calculation Mode', items = calculation_mode_items, update = lambda s,c:s.update_config( ))

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )

    def define_sockets( self ):
        return{
            'input_texture' : I( 'sampler2D', 'Texture' ),
            'uv' : I( 'vec2', 'UV', default = 'UV[0]' ),
            'radius' : I( 'float', 'Radius', default = 5.0 ),
            'ratio' : I( 'float', 'Ratio', default = 0.01 ),
            'box_circular' : I( 'bool', 'Circular', default = False ),
            'jitter_exponent' : I( 'float', 'Exponent', default = 5.0 ),
            'jitter_samples' : I( 'int', 'Samples', default = 8 ),
            'gaussian_sigma' : I( 'float', 'Sigma', default = 5.0 ),
            'result' : O( 'vec4', 'Result' )
        }
    
    def update_socket_visibility( self ):
        bm = self.blur_mode
        cm = self.calculation_mode
        self.inputs[ 'box_circular' ].enabled = bm == 'BOX'
        self.inputs[ 'jitter_exponent' ].enabled = bm == 'JITTER'
        self.inputs[ 'jitter_samples' ].enabled = bm == 'JITTER'
        self.inputs[ 'gaussian_sigma' ].enabled = bm == 'GAUSSIAN'

        self.inputs[ 'radius' ].enabled = cm == 'ABSOLUTE'
        self.inputs[ 'ratio' ].enabled = cm == 'RATIO'
    
    def get_function( self ):
        f = ''
        if self.calculation_mode == 'RATIO':
            f += 'radius = get_texture_size( input_texture ) * ratio;\n'

        f += {
            'BOX' : 'result = box_blur( input_texture, uv, radius, box_circular );\n',
            'JITTER' : 'result = jitter_blur( input_texture, uv, radius, jitter_exponent, jitter_samples );\n',
            'GAUSSIAN' : 'result = gaussian_blur( input_texture, uv, radius, gaussian_sigma );\n'
        }[ self.blur_mode ]
        return f
    
    def draw_buttons(self, context, layout ):
        c = layout.column( align = True )
        c.prop( self, 'blur_mode', text = '' )
        c.prop( self, 'calculation_mode', text = '' )
        

NODES = [ MaltNodeTexBlur ]
    
