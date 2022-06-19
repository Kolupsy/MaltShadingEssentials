import bpy

from ..custom_malt import CustomFunctionNode, MaltVariableIn as I, MaltVariableOut as O, enum_from_rna

class EssentialsTemplate( ):

    menu_category = 'INPUT'
    tooltip = ''
    default_width = None

    def malt_init( self ):
        result = super( ).malt_init( )
        if not self.default_width == None:
            self.width = self.default_width
        self.on_init( )
        self.update_socket_visibility( )
        return result
    
    def on_init( self ):
        pass

    @classmethod
    def get_category_data( cls ) -> dict:
        return {
            'OTHER' : ( 'Other', ( 0.25, 0.25, 0.25 ), 'NONE' ),
            'INPUT' : ( 'Input', ( 0.15, 0.34, 0.3 ), 'FORWARD' ),
            'OUTPUT': ( 'Output', ( 0.38, 0.05, 0.2 ), 'RENDER_RESULT' ),
            'PRIMITIVES' : ( 'Primitives', ( 0.34, 0.18, 0.27 ), 'NONE' ),
            'SHADER': ( 'Shader', ( 0.04, 0.29, 0.09 ), 'SHADING_RENDERED' ),
            'COLOR' : ( 'Color', ( 0.69, 0.48, 0.002 ), 'COLOR' ),
            'TEXTURE':( 'Texture', ( 0.57, 0.21, 0.05 ), 'TEXTURE' ),
            'CONVERTOR':( 'Convertor', ( 0.13, 0.22, 0.4 ), 'CON_TRANSFORM' ),
            'VECTOR' : ( 'Vector', ( 0.15, 0.03, 0.41 ), 'CON_TRANSLIKE' ),
        }

    @classmethod
    def parse_category( cls ):

        category_data = cls.get_category_data( )
        if not cls.menu_category in category_data:
            return category_data[ 'OTHER' ]
        else:
            return category_data[ cls.menu_category ]

def malt_update( self:EssentialsTemplate, context ):
    self.update_tree( )

def socket_update( self:EssentialsTemplate, context ):
    self.update_socket_visibility( )

class EssentialsNode( EssentialsTemplate, CustomFunctionNode ):
    pass

__all__ = [ 'EssentialsNode', 'I', 'O', 'bpy', 'enum_from_rna', 'malt_update', 'socket_update' ]