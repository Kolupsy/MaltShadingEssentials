from bpy.props import *
from .utils import *
from .tex_noise import dimensions_items, socket_visibility

voronoi_rna = bpy.types.ShaderNodeTexVoronoi.bl_rna
dimensions_items = enum_from_rna( voronoi_rna, 'voronoi_dimensions' )
feature_items = enum_from_rna( voronoi_rna, 'feature' )
distance_items = enum_from_rna( voronoi_rna, 'distance' )

class MaltNodeTexVoronoi( EssentialsNode ):
    bl_idname = 'MaltNodeTexVoronoi'
    bl_label = 'Voronoi Texture'
    menu_category = 'TEXTURE'
    default_width = 155

    voronoi_dimensions : EnumProperty( name = 'Dimensions', items = dimensions_items, default = '2D', update = lambda s,c:s.update_config( ))
    feature : EnumProperty( name = 'Feature', items = feature_items, default = 'F1', update = lambda s,c:s.update_config( ))
    distance : EnumProperty( name = 'Distance', items = distance_items, default = 'EUCLIDEAN', update = lambda s,c:s.update_config( ))

    def update_socket_visibility( self ):
        for i in ( x for x in self.inputs if x.name in socket_visibility.values( )):
            i.enabled = i.name == socket_visibility[ self.voronoi_dimensions ]

        self.inputs[ 'smoothness' ].enabled = self.feature == 'SMOOTH_F1'
        self.inputs[ 'exponent' ].enabled = self.distance == 'MINKOWSKI' and not self.feature in [ 'DISTANCE_TO_EDGE', 'N_SPHERE_RADIUS' ]

        self.outputs[ 'distance' ].enabled = self.feature != 'N_SPHERE_RADIUS'
        self.outputs[ 'outColor' ].enabled = self.feature not in [ 'DISTANCE_TO_EDGE', 'N_SPHERE_RADIUS' ]
        self.outputs[ 'position' ].enabled = self.feature not in [ 'DISTANCE_TO_EDGE', 'N_SPHERE_RADIUS' ] and self.voronoi_dimensions != '1D'
        self.outputs[ 'coords' ].enabled = self.feature not in [ 'DISTANCE_TO_EDGE', 'N_SPHERE_RADIUS' ] and self.voronoi_dimensions != '1D'
        self.outputs[ 'w' ].enabled = self.feature not in [ 'DISTANCE_TO_EDGE', 'N_SPHERE_RADIUS' ] and self.voronoi_dimensions == '1D'
        self.outputs[ 'radius' ].enabled = self.feature == 'N_SPHERE_RADIUS'
    
    def update_config( self ):
        self.update_socket_visibility( )
        self.update_tree( )
    
    def define_sockets( self ):
        return{
            'fac' : I( 'float', 'Fac', default = 0.0 ),
            'uv' : I( 'vec2', 'UV', default = 'surface_uv( 0 )' ),
            'vector' : I( 'vec3', 'Vector', default = 'object_coords( )' ),
            'color' : I( 'vec4', 'Color', default = 'vec4( object_coords( ), 1.0 )' ),

            'scale' : I( 'float', 'Scale', default = 5.0 ),
            'smoothness' : I( 'float', 'Smooth', min = 0.0, max = 1.0, default = 1.0 ),
            'exponent' : I( 'float', 'Exponent', min = 0.0, default = 0.5 ),
            'randomness' : I( 'float', 'Random', min = 0.0, max = 1.0, default = 1.0 ),

            'distance' : O( 'float', 'Distance' ),
            'outColor' : O( 'vec4', 'Color' ),
            'position' : O( 'vec3', 'Position' ),
            'coords'   : O( 'vec3', 'Coords' ),
            'w' : O( 'float', 'W' ),
            'radius' : O( 'float', 'Radius' )
        }
    
    def get_function( self ):
        func_name = 'voronoi_texture_'
        func_name += {
            'DISTANCE_TO_EDGE' : 'distance_to_edge_',
            'N_SPHERE_RADIUS' : 'n_sphere_radius_',
            'F1' : 'f1_',
            'F2' : 'f2_',
            'SMOOTH_F1' : 'smooth_f1_',
        }[ self.feature ]
        func_name += {
            '1D' : '1d',
            '2D' : '2d',
            '3D' : '3d',
            '4D' : '4d'
        }[ self.voronoi_dimensions ]
        metric = {
            'EUCLIDEAN' : 0.0,
            'MANHATTAN' : 1.0,
            'CHEBYCHEV' : 2.0,
            'MINKOWSKI' : 3.0,
        }[ self.distance ]
        input_socket_name = socket_visibility[ self.voronoi_dimensions ]
        f = f'{func_name}( {input_socket_name}, scale, smoothness, exponent, randomness, {metric}, distance, outColor, position, w, radius );\n'
        if not self.feature in [ 'DISTANCE_TO_EDGE', 'N_SPHERE_RADIUS' ] and self.voronoi_dimensions != '1D':
            converted_input = {
                '2D' : 'vec3( uv, 0.0 )',
                '3D' : 'vector',
                '4D' : 'color.xyz'
            }[ self.voronoi_dimensions ]
            f += f'coords = ( {converted_input} - position ) * vec3( scale );\n'
        return f

    def draw_buttons( self, context, layout ):
        c = layout.column( align = True )
        c.prop( self, 'voronoi_dimensions', text = '' )
        c.prop( self, 'feature', text = '' )
        if self.feature in [ 'F1', 'F2', 'SMOOTH_F1' ]:
            c.prop( self, 'distance', text = '' )

NODES = [ MaltNodeTexVoronoi ]