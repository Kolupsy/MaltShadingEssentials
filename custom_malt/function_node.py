import bpy
import rna_prop_ui

from bpy.props import EnumProperty, StringProperty
from .node import MaltCustomNode

def PrimitiveTypeProperty( **args ):
    args.setdefault( 'name', 'Data Type' )
    items = [
        ( 'float', 'Float', 'Float' ),
        ( 'vec2', 'Vec2', 'Vec2' ),
        ( 'vec3', 'Vec3', 'Vec3' ),
        ( 'vec4', 'Vec4', 'Vec4' ),
    ]
    return EnumProperty( **args, items = items )

def enum_from_rna( rna, prop_name ):
    return[( x.identifier, x.name, x.description ) for x in rna.properties[prop_name].enum_items ]

def peel_value( value ):
    try:
        len( value )
        return [ peel_value( x ) for x in value ]
    except TypeError:
        return value

class CustomFunctionNode( bpy.types.Node, MaltCustomNode ):
    '''Run a custom shader function from this node.

    def define_sockets( self ) -> dict  # Values as MaltVariable subclass
    def get_function( self ) -> str     # As valid glsl code
    '''
    bl_idname = 'MaltCustomStaticNode'
    bl_label = 'Custom Static Node'

    def malt_setup( self ):
        super( ).malt_setup( )
        for param_name, data in self.get_inputs( ).items( ):
            params = self.malt_parameters
            meta = data[ 'meta' ]
            if type( meta.get( 'default', None )) == str:
                continue #Sockets without exposed values dont need min/max
            try:
                old_id_ui = params.id_properties_ui( param_name ).as_dict( )
            except:
                continue #some properties can not have UIs and dont need min/max
            set_value = peel_value( params[ param_name ])
            rna_prop_ui.rna_idprop_ui_create( 
                params, 
                param_name, 
                default = meta.get( 'default', old_id_ui[ 'default' ]),
                min = meta.get( 'min', old_id_ui[ 'min' ]),
                max = meta.get( 'max', old_id_ui[ 'max' ]),
                )
            params[ param_name ] = set_value
            rna_prop_ui.rna_idprop_ui_prop_update( params, param_name )

    def get_function_wrapper( self ):
        header = '\n'
        inputs = self.get_inputs( ).items( )
        outputs = self.get_outputs( ).items( )
        for name, dic in outputs:
            type = dic['type']
            var = self.outputs[name].get_source_reference( )
            header += f'{type} {var};\n'
        header += '{{\n'
        for name, dic in inputs:
            type = dic['type']
            var = self.inputs[ name ].get_source_initialization( )
            header += f'{type} {name} = {var};\n'
        for name, dic in outputs:
            type = dic['type']
            header += f'{type} {name};\n'
        header += '{func}'
        for name, type in outputs:
            var = self.outputs[name].get_source_reference( )
            header += f'{var} = {name};\n'
        header += '}}'
        return header
    
    def get_source_code( self, transpiler ):
        func = self.get_function( )
        if not type( func ) == str:
            raise TypeError( 'CustomFunctionNode function has to be string type' )
        return self.get_function_wrapper( ).format( func = self.get_function( ))

    def draw_socket( self, context, layout, socket, text ):
        super( ).draw_socket( context, layout, socket, self.draw_socket_name( socket ))
        if socket.is_output:
            return
        if socket.is_linked:
            return
        if ( default := socket.default_initialization ) == '':
            return
        MaltShadingEssentials_OT_socket_info.draw_ui( layout, f'Default: {default}' )
    
    def draw_socket_name( self, socket ):
        if socket.is_struct_member( ):
            struct_socket = socket.get_struct_socket( )
            name = socket.name.split( '.' )[-1]
            return f'{self.draw_socket_name( struct_socket)}.{name}'
        else:
            return self.define_sockets( )[ socket.identifier ].name
    
    def get_inputs( self ):
        d = { }
        for key, var in self.define_sockets( ).items( ):
            if not var.is_out:
                d[ key ] = var.get_dict( )
        return d

    def get_outputs( self ):
        d = { }
        for key, var in self.define_sockets( ).items( ):
            if var.is_out:
                d[ key ] = var.get_dict( )
        return d
    
    def get_function( self ):
        return None

    def define_sockets( self ):
        return {}

class MaltShadingEssentials_OT_socket_info( bpy.types.Operator ):
    bl_idname = 'maltshadingessentials.socket_info'
    bl_label = 'Socket Info'
    bl_options = {'INTERNAL'}

    text : StringProperty( )


    @classmethod
    def poll( cls, context ):
        return True
    
    @classmethod
    def description( cls, context, properties ) -> str:
        return properties.text

    def execute( self, context ):
        print( self.text )
        return{ 'FINISHED' }
    
    @staticmethod
    def draw_ui( layout, text:str ):
        op = layout.operator( MaltShadingEssentials_OT_socket_info.bl_idname, text = '', icon = 'DOT', emboss = False )
        op.text = text