import glob, bpy
from os.path import dirname
from .utils import EssentialsNode
from typing import List
from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

_all_modules = glob.glob( '*.py', root_dir = dirname( __file__ ))
__all__ = [ x.rsplit( '.py', 1 )[0] for x in _all_modules if not x.startswith( '__' )]

PACKAGE_ID = 'MALTSHADINGESSENTIALS'

from . import *

modules = [ globals( )[ x ] for x in __all__ ]

def get_all_nodes( ) -> List[EssentialsNode]:
    node_classes = []
    for m in modules:
        node_classes += getattr( m, 'NODES', [])
    return node_classes

def get_node_draw_item( cls ):
    def draw( self, context ):
        l = self.layout
        o = l.operator( 'node.add_node', text = cls.bl_label )
        o.type = cls.bl_idname
        o.use_transform = True
    return draw

draw_items = [ get_node_draw_item( x ) for x in get_all_nodes( )]

class EssentialsNodeCategory( NodeCategory ):
    @classmethod
    def poll( cls, context ):
        return(
            context and
            getattr( context.space_data, 'type', '' ) == 'NODE_EDITOR' and
            getattr( context.space_data, 'edit_tree', None ) and
            getattr( context.space_data.edit_tree, 'bl_idname', '' ) == 'MaltTree'
        )

def register_categories( register ):
    if register:
        category_data = EssentialsNode.get_category_data( )
        cat_list = []
        for identifier in category_data.keys( ):
            data = category_data[ identifier ]
            nodes = [ x for x in get_all_nodes( ) if x.menu_category == identifier ]
            nodes.sort( key = lambda x: x.bl_label )
            if not nodes:
                continue
            node_items = [ NodeItem( x.bl_idname, settings = {'use_custom_color':repr(True), 'color':repr(data[1]), 'bl_icon':repr(data[2])}) for x in nodes ]
            cat_list.append( EssentialsNodeCategory( f'{PACKAGE_ID}_{identifier}', f'[SE] {data[0]}', items = node_items ))
        register_node_categories( PACKAGE_ID, cat_list )
    else:
        unregister_node_categories( PACKAGE_ID )

# CLASSES = get_all_nodes( )
# REGISTER = [
#     register_categories,
# ]