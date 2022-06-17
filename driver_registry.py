import bpy
from bpy.props import *
from typing import Any

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

class MaltShadingEssentialsDriverRegistry( bpy.types.PropertyGroup ):

    registry : CollectionProperty( type = DriverRegistryItem )

    def add_item( self, node:bpy.types.Node, malt_prop_name:str, source_obj:Any, source_prop_name:str ) -> DriverRegistryItem:
        a = self.registry.add( )
        a.node_pointer.obj = node
        a.malt_prop_name = malt_prop_name
        a.source_pointer.obj = source_obj
        a.source_prop_name = source_prop_name
        return a
    
    def remove_item( self, node:bpy.types.Node, malt_prop_name:str ):
        if self.has_item( node, malt_prop_name ):
            index = next( i for i, x in enumerate( self.registry ) if x.node_pointer.obj == node and x.malt_prop_name == malt_prop_name )
            self.registry.remove( index )
    
    def has_item( self, node:bpy.types.Node, malt_prop_name:str ):
        return any( x.node_pointer.obj == node and x.malt_prop_name == malt_prop_name for x in self.registry )

def register_driver_registry( register ):
    wm = bpy.types.WindowManager
    if register:
        wm.malt_shading_essentials_drivers = PointerProperty( type = MaltShadingEssentialsDriverRegistry, name = 'Shading Essentials Drivers' )
    else:
        del wm.malt_shading_essentials_drivers

CLASSES = [
    IndirectPointer,
    DriverRegistryItem,
    MaltShadingEssentialsDriverRegistry,
]

REGISTER = [
    register_driver_registry
]
