import bpy
from bpy.props import *
from typing import Any
import rna_prop_ui
from bpy.app import handlers

class IndirectPointer( bpy.types.PropertyGroup ):

    id_obj : PointerProperty( type = bpy.types.ID )
    path : StringProperty( )

    @property
    def obj( self ):
        pass
    
    @obj.getter
    def obj( self ):
        if self.path == '':
            return self.id_obj
        else:
            return self.id_obj.path_resolve( self.path )

    @obj.setter
    def obj( self, target_obj:bpy.types.bpy_struct ):
        self.id_obj = target_obj.id_data
        if self.id_obj == target_obj:
            self.path = ''
        else:
            self.path = target_obj.path_from_id( )

class DriverRegistryItem( bpy.types.PropertyGroup ):

    node_pointer : PointerProperty( type = IndirectPointer )
    malt_prop_name : StringProperty( )

    source_pointer : PointerProperty( type = IndirectPointer )
    source_prop_name : StringProperty( )

    update_callback : StringProperty( )

    def update_target( self ) -> None:
        node = self.node_pointer.obj
        source = self.source_pointer.obj
        result = getattr( source, self.source_prop_name )
        if self.update_callback == '':
            node.malt_parameters[ self.malt_prop_name ] = result
            rna_prop_ui.rna_idprop_ui_prop_update( node.malt_parameters, self.malt_prop_name )
        else:
            updates = getattr( node, self.update_callback )( result )
            for u in updates:
                rna_prop_ui.rna_idprop_ui_prop_update( node.malt_parameters, u )
    
    def is_driver_valid( self ) -> bool:
        try:
            return self.node_pointer.obj != None and self.source_pointer.obj != None
        except ValueError:
            return False
        except TypeError:
            return False

class MaltShadingEssentialsDriverRegistry( bpy.types.PropertyGroup ):

    registry : CollectionProperty( type = DriverRegistryItem )

    def add_item( self, node:bpy.types.Node, malt_prop_name:str, source_obj:Any, source_prop_name:str, update_callback:str = '' ) -> DriverRegistryItem:
        a:DriverRegistryItem = self.registry.add( )
        a.node_pointer.obj = node
        a.malt_prop_name = malt_prop_name
        a.source_pointer.obj = source_obj
        a.source_prop_name = source_prop_name
        a.update_callback = update_callback
        a.update_target( )
        return a
    
    def get_item( self, node:bpy.types.Node, malt_prop_name:str ):
        if self.has_item( node, malt_prop_name ):
            return next( x for x in self.registry if x.node_pointer.obj == node and x.malt_prop_name == malt_prop_name )
        else:
            raise ValueError( f'Driver using {node} with Malt Parameter "{malt_prop_name}" does not exist' )
    
    def remove_item( self, item:DriverRegistryItem ):
        self.registry.remove( next( i for i, x in enumerate( self.registry ) if x == item ))
    
    def has_item( self, node:bpy.types.Node, malt_prop_name:str ):
        return any( x.node_pointer.obj == node and x.malt_prop_name == malt_prop_name for x in self.registry )

def register_driver_registry( register ):
    wm = bpy.types.WindowManager
    if register:
        wm.malt_shading_essentials_drivers = PointerProperty( type = MaltShadingEssentialsDriverRegistry, name = 'Shading Essentials Drivers' )
    else:
        del wm.malt_shading_essentials_drivers

@handlers.persistent
def persistent_registry_update( *_args ):
    drivers:MaltShadingEssentialsDriverRegistry = bpy.context.window_manager.malt_shading_essentials_drivers
    for item in drivers.registry:
        item:DriverRegistryItem
        if item.is_driver_valid( ):
            item.update_target( )
        else:
            drivers.remove_item( item )

def register_persistent_update( register ):
    for handler in ( handlers.depsgraph_update_pre, handlers.frame_change_pre, handlers.render_pre ):
        getattr( handler, 'append' if register else 'remove' )( persistent_registry_update )

CLASSES = [
    IndirectPointer,
    DriverRegistryItem,
    MaltShadingEssentialsDriverRegistry,
]

REGISTER = [
    register_driver_registry,
    register_persistent_update
]