from .utils import *

class MaltNodeVertexColor( EssentialsNode ):
    bl_idname = 'MaltNodeVertexColor'
    bl_label = 'Vertex Color'
    menu_category = 'INPUT'

    def define_sockets( self ):
        return{
            'index' : I( 'int', 'Index', default = 0, min = 0.0 ),
            'color' : O( 'vec4', 'Color' )
        }
    
    def get_function( self ):
        return 'color = surface_vertex_color( index );\n'

NODES = [ MaltNodeVertexColor ]