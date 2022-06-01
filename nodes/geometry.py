from bpy.props import *
from .utils import *

class MaltNodeGeometry( EssentialsNode ):
    bl_idname = 'MaltNodeGeometry'
    bl_label = 'Geometry'
    menu_category = 'INPUT'
    default_width = 150
    
    def define_sockets( self ):
        return{
            'position' : O( 'vec3', 'Position' ),
            'normal' : O( 'vec3', 'Normal' ),
            'tangent' : O( 'vec3', 'Tangent' ),
            'true_normal' : O( 'vec3', 'True Normal' ),
            'incoming' : O( 'vec3', 'Incoming' ),
            'parametric' : O( 'vec2', 'TODO:Parametric' ),
            'backfacing' : O( 'float', 'Backfacing' ),
            'curvature' : O( 'float', 'Curvature' ),
            'random_island' : O( 'float', 'TODO:Random Per Island' )
        }
    
    def get_function( self ):
        return 'geometry_info( position, normal, tangent, true_normal, incoming, parametric, backfacing, curvature, random_island );\n'

NODES = [ MaltNodeGeometry ]