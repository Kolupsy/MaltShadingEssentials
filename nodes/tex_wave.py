from .utils import *
from bpy.props import *

wave_rna = bpy.types.ShaderNodeTexWave.bl_rna

wave_type_items = enum_from_rna( wave_rna, 'wave_type' )
wave_profile_items = enum_from_rna( wave_rna, 'wave_profile' )

class MaltNodeTexWave( EssentialsNode ):
    bl_idname = 'MaltNodeTexWave'
    bl_label = 'Wave Texture'
    menu_category = 'TEXTURE'

    wave_type : EnumProperty( name = 'Wave Type', items = wave_type_items, update = lambda s,c:s.update_config( ))
    wave_profile : EnumProperty( name = 'Wave Profile', items = wave_profile_items, update = lambda s,c:s.update_config( ))

    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )

    def update_socket_visibility( self ):
        
        is_rings = self.wave_type == 'RINGS'
        self.inputs[ 'w' ].enabled = not is_rings
        self.inputs[ 'vector' ].enabled = is_rings

    def define_sockets( self ):
        return{
            'w' : I( 'float', 'W', default = 'float(0.0)' ),
            'vector' : I( 'vec3', 'Vector', default = 'object_coords( )' ),
            'scale' : I( 'float', 'Scale', default = 5.0 ),
            'phase' : I( 'float', 'Phase', default = 0.0 ),
            'waves' : O( 'float', 'Waves' ),
        }
    
    def get_function( self ):
        
        func_name = {
            'SIN' : 'texture_wave_sine',
            'SAW' : 'texture_wave_saw',
            'TRI' : 'texture_wave_triangle'
        }[ self.wave_profile ]
        f = 'float mapping;\n'
        if self.wave_type == 'RINGS':
            f += 'mapping = length( vector );\n'
        else:
            f += 'mapping = w;\n'
        f += f'waves = {func_name}( mapping, scale, phase );\n'
        return f

    def draw_buttons( self, context, layout ):
        c = layout.column( align = True )
        c.prop( self, 'wave_type', text = '' )
        c.prop( self, 'wave_profile', text = '' )
    
NODES = [ MaltNodeTexWave ]