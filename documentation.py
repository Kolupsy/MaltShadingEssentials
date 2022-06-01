from dataclasses import dataclass
import pathlib

MAINDIR = pathlib.Path( __file__ ).parent

from .nodes import get_all_nodes
from .nodes.utils import EssentialsNode

CAT_DATA = EssentialsNode.get_category_data( )

@dataclass
class LibraryItem( object ):

    label:str
    idname:str
    category:str
    path:str

    @property
    def category_name( self ):
        return CAT_DATA[ self.category ][0]

    @property
    def order_id( self ):
        number = f'{next( i for i,x in enumerate( CAT_DATA.keys( )) if self.category == x ):03}'
        return f'{number}{self.label}'
    
    def get_formatted( self ):
        return f'- {self.label} / {self.idname} : [{self.path}]\n'

def generate_library( ):

    nodes = get_all_nodes( )
    library = {}
    for key in CAT_DATA.keys( ):
        library[ key ] = []
    
    for n in nodes:
        idname = n.bl_idname
        label = n.bl_label
        path = '/'.join( n.__module__.split( '.' )[-2:]) + '.py'
        item = LibraryItem( label, idname, n.menu_category, path )

        library[ n.menu_category ].append( item )

    text = '# Shader Nodes\n\n'

    for key, items in library.items( ):
        if not items:
            continue
        text += f'**{CAT_DATA[ key ][ 0 ]}:**\n'
        for i in items:
            text += i.get_formatted( )
        text += '\n'

    with open( MAINDIR.joinpath( 'LIBRARY.md' ), 'w' ) as open_file:
        open_file.write( text )
