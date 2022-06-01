from bpy.props import *
from .utils import *

rotatenode_rna = bpy.types.ShaderNodeVectorRotate.bl_rna
rotation_type_items = enum_from_rna( rotatenode_rna, 'rotation_type' )

class MaltNodeVectorRotate( EssentialsNode ):
    bl_idname = 'MaltNodeVectorRotate'
    bl_label = 'Rotate'
    menu_category = 'VECTOR'
    default_width = 160

    rotation_type : EnumProperty( name = 'Type', items = rotation_type_items, default = 'AXIS_ANGLE', update = lambda s,c: s.update_type( ))
    invert : BoolProperty( name = 'Invert', default = False, update = lambda s,c: s.update_type( ))
    
    def update_type( self ):
        self.update_socket_visibility( )
        self.update_tree( )

    def update_socket_visibility( self ):
        self.inputs[ 'axis' ].enabled = self.rotation_type == 'AXIS_ANGLE'
        use_euler = self.rotation_type == 'EULER_XYZ'
        self.inputs[ 'angle' ].enabled = not use_euler
        self.inputs[ 'rotation' ].enabled = use_euler
        self.update_tree( )

    def define_sockets( self ):
        return{
            'vector' : I( 'vec3', 'Vector', default = 'vec3( 0.0 )' ),
            'center' : I( 'vec3', 'Center', default = 'vec3( 0.0 )' ),
            'axis' : I( 'vec3', 'Axis', subtype = 'Vector', default = ( 0.0,0.0,1.0 )),
            'angle' : I( 'float', 'Angle', subtype = 'Degrees' ),
            'rotation' : I( 'vec3', 'Rotation', subtype = 'Vector' ),
            'result' : O( 'vec3', 'Vector' )
        }
    
    def get_function( self ):
        f = ''
        f += 'vector = vector - center;\n'
        f += 'mat4 matrix;\n'
        if self.rotation_type == 'EULER_XYZ':
            f += 'matrix = mat4_rotation_from_euler( rotation );\n'
        else:
            axis = {
                'X_AXIS' : 'vec3(1,0,0)',
                'Y_AXIS' : 'vec3(0,1,0)',
                'Z_AXIS' : 'vec3(0,0,1)',
                'AXIS_ANGLE' : 'axis'
            }[ self.rotation_type ]
            f += f'matrix = rotation_matrix_axis_angle( {axis}, angle );\n'
        if self.invert:
            f += f'matrix = inverse( matrix );\n'
        f += 'result = transform_direction( matrix, vector );\n'
        f += 'result = result + center;\n'
        return f

    def draw_buttons( self, context, layout ):
        r = layout.row( align = True )
        r.prop( self, 'rotation_type', text = '' )
        r.prop( self, 'invert', text = '', icon = 'LOOP_FORWARDS' if self.invert else 'LOOP_BACK' )

NODES = [ MaltNodeVectorRotate ]