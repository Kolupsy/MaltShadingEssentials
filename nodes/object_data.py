from .utils import *
from bpy.props import *
from ..driver_registry import MaltShadingEssentialsDriverRegistry, DriverRegistryItem
from mathutils import Matrix
import rna_prop_ui

class MaltNodeObjectData( EssentialsNode ):
    bl_idname = 'MaltNodeObjectData'
    bl_label = 'Object Data'
    menu_category = 'INPUT'
    default_width = 170

    source_object : PointerProperty( type = bpy.types.Object, name = 'Source Object', update = lambda s,c:s.update_object( ))
    expose_vector : BoolProperty( name = 'Expose Vector', default = False, update = socket_update )

    def get_drivers( self ) -> MaltShadingEssentialsDriverRegistry:
        return bpy.context.window_manager.malt_shading_essentials_drivers
    
    def clear_driver( self ) -> None:
        drivers = self.get_drivers( )
        if drivers.has_item( self, 'in_location' ):
            d = drivers.get_item( self, 'in_location' )
            drivers.remove_item( d )

    def update_object( self ) -> None:
        drivers = self.get_drivers( )
        self.clear_driver( )

        if self.source_object:
            drivers.add_item( self, 'in_location', self.source_object, 'matrix_world', update_callback = 'update_props' )
    
    def update_props( self, mat:Matrix ) -> tuple:

        self.malt_parameters[ 'in_location' ] = mat.translation
        self.malt_parameters[ 'in_rotation' ] = mat.to_euler( )
        self.malt_parameters[ 'in_scale' ] = mat.to_scale( )
        return 'in_location', 'in_rotation', 'in_scale'
    
    def copy( self, node ):
        self.update_object( )
    def free( self ):
        self.clear_driver( )

    def update_socket_visibility( self ):
        for n in [ 'in_location', 'in_rotation', 'in_scale' ]:
            self.inputs[ n ].enabled = False
        self.inputs[ 'in_vector' ].enabled = self.expose_vector

    def define_sockets( self ):
        return{
            'in_vector' : I( 'vec3', 'Vector', subtype = 'Vector', default = ( 0.0, 0.0, 1.0 )),
            'in_location' : I( 'vec3', 'Location' ),
            'in_rotation' : I( 'vec3', 'Rotation' ),
            'in_scale' : I( 'vec3', 'Scale' ),
            'out_location' : O( 'vec3', 'Location' ),
            'out_rotation' : O( 'vec3', 'Rotation' ),
            'out_scale' : O( 'vec3', 'Scale' ),
            'mapping' : O( 'vec3', 'Mapping' ),
            'vector' : O( 'vec3', 'Vector' ),
            'ss_orientation' : O( 'vec2', 'Screen Orientation' ),
        }
    
    def get_function( self ):
        f = 'out_location = in_location; out_rotation = in_rotation; out_scale = in_scale;\n'
        f += 'mapping = vector_mapping_texture( POSITION, in_location, in_rotation, in_scale );\n'
        f += 'vector = vector_mapping_vector( in_vector, in_rotation, in_scale );\n'
        f += 'ss_orientation = object_view_orientation( in_vector, in_location, in_rotation, in_scale );\n'
        return f
    
    def draw_buttons( self, context, layout ):
        r = layout.row( align = True )
        r.prop( self, 'source_object', text = '' )
        r.prop( self, 'expose_vector', text = '', icon = 'EMPTY_SINGLE_ARROW' )

NODES = [ MaltNodeObjectData ]