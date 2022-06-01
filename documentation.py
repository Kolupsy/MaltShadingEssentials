import pathlib

MAINDIR = pathlib.Path( __file__ ).parent

from .nodes import get_all_nodes
from .nodes.utils import EssentialsNode

CAT_DATA = EssentialsNode.get_category_data( )

class LibraryItem( object ):

    node_clss = None

    def __init__( self, node_clss ):
        self.node_clss = node_clss

    @property
    def label( self ):
        return self.node_clss.bl_label
    @property
    def idname( self ):
        return self.node_clss.bl_idname
    @property
    def path( self ):
        return '/'.join( self.node_clss.__module__.split( '.' )[-2:]) + '.py'
    @property
    def category_name( self ):
        return CAT_DATA[ self.category ][0]
    @property
    def formatted( self ):
        f = f'- {self.label} / {self.idname} : [{self.path}]\n'
        if self.valid_tooltip( ):
            f += '\t'
            formatted_tooltip = self.node_clss.tooltip
            while formatted_tooltip[0] in [ '\n', '\t', ' ' ]:
                formatted_tooltip = formatted_tooltip[1:]
            while formatted_tooltip[-1] in [ '\n', '\t', ' ' ]:
                formatted_tooltip = formatted_tooltip[:-1]
            formatted_tooltip = formatted_tooltip.replace( '\n', '\n\t' )
            f += formatted_tooltip
            f += '\n'
        return f
    
    def valid_tooltip( self ):
        t = self.node_clss.tooltip
        return not t == '' and not all( x in [ ' ', '\n', '\t' ] for x in t )

def generate_library( ):

    nodes = get_all_nodes( )
    library = {}
    for key in CAT_DATA.keys( ):
        library[ key ] = []
    
    for n in nodes:

        library[ n.menu_category ].append( LibraryItem( n ))

    text = '# Shader Nodes\n\n'

    for key, items in library.items( ):
        if not items:
            continue
        text += f'**{CAT_DATA[ key ][ 0 ]}:**\n'
        for i in items:
            text += i.formatted
        text += '\n'

    with open( MAINDIR.joinpath( 'LIBRARY.md' ), 'w' ) as open_file:
        open_file.write( text )
    
    return library
