import pathlib

MAINDIR = pathlib.Path( __file__ ).parent

from .nodes import get_all_nodes
from .nodes.utils import EssentialsNode

CAT_DATA = EssentialsNode.get_category_data( )

def get_all_pipeline_nodes( ) -> list[object]:
    import importlib, sys
    result = []
    pipeline_nodes_path = pathlib.Path( __file__ ).parent.joinpath( 'PipelineNodes' )
    if not str( pipeline_nodes_path ) in sys.path:
        sys.path.append( str( pipeline_nodes_path ))
    pipeline_nodes = [ x.stem for x in pipeline_nodes_path.glob( '*.py' ) if not x.name == '__init__.py' ]
    for node_module_name in pipeline_nodes:
        m = importlib.import_module( node_module_name )
        if hasattr( m, 'NODE' ):
           result.append( m.NODE )

    return result 
        
class LibraryItem( object ):

    node_clss = None

    def __init__( self, node_clss ):
        self.node_clss = node_clss

    @property
    def label( self ):
        return getattr( self.node_clss, 'bl_label', self.node_clss.__name__ )
    @property
    def idname( self ):
        return getattr( self.node_clss, 'bl_idname', self.node_clss.__name__ )
    @property
    def tooltip( self ):
        return getattr( self.node_clss, 'tooltip', '' )
    @property
    def path( self ):
        return '/'.join( self.node_clss.__module__.split( '.' )[-2:]) + '.py'

    def format_tooltip( self ):
        formatted_tooltip = self.tooltip
        while formatted_tooltip[0] in [ '\n', '\t', ' ' ]:
            formatted_tooltip = formatted_tooltip[1:]
        while formatted_tooltip[-1] in [ '\n', '\t', ' ' ]:
            formatted_tooltip = formatted_tooltip[:-1]
        formatted_tooltip = formatted_tooltip.replace( '\n', '\n\t' )
        return formatted_tooltip

    @property
    def formatted( self ):
        f = f'- {self.label} / {self.idname} : [{self.path}]\n'
        if self.valid_tooltip( ):
            f += '\t'
            f += self.format_tooltip( )
            f += '\n'
        return f
    
    def valid_tooltip( self ):
        t = self.tooltip
        return not t == '' and not all( x in [ ' ', '\n', '\t' ] for x in t )

def generate_library( ):

    nodes = get_all_nodes( )
    library = { key : [] for key in CAT_DATA.keys( )}
    
    for n in nodes:
        library[ n.menu_category ].append( LibraryItem( n ))
    for n in get_all_pipeline_nodes( ):
        library[ 'OTHER' ].append( LibraryItem( n ))

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
