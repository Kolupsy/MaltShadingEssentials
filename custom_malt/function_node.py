from bpy.types import Node
import importlib

from bpy.props import EnumProperty
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

class CustomFunctionNode( Node, MaltCustomNode ):
    '''Run a custom shader function from this node.

    def define_sockets( self ) -> dict  # Values as MaltVariable subclass
    def get_function( self ) -> str     # As valid glsl code
    '''
    bl_idname = 'MaltCustomStaticNode'
    bl_label = 'Custom Static Node'

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
    
    def draw_socket_name( self, socket ):
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
