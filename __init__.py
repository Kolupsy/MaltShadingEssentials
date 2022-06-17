import os, glob
from Malt.PipelinePlugin import PipelinePlugin, isinstance_str

def get_modules( ):

    all_modules = glob.glob( '*.py', root_dir = os.path.dirname( __file__ ))
    __all__ = [ x.rsplit( '.py', 1 ) for x in all_modules if not x.startswith( '__' )]
    from . import nodes
    from . import driver_registry
    return [ nodes, driver_registry ]

def module_register( register, debug = False ):
    import bpy
    class_register = getattr( bpy.utils, 'register_class' if register else 'unregister_class' )
    for m in get_modules( ):
        for c in getattr( m, 'CLASSES', [ ]):
            if debug:
                print( f'{"Register" if register else "Unregister"} Class: {c.__name__}')
            class_register( c )

        for func in getattr( m, 'REGISTER', [ ]):
            if debug:
                print( f'{"Registering" if register else "Unregistering"} function {func}')
            func( register )

class ShadingEssentialsPlugin( PipelinePlugin ):

    @classmethod
    def poll_pipeline( cls, pipeline ):
        return isinstance_str(pipeline, 'NPR_Pipeline')
    
    @classmethod
    def register_graph_libraries( cls, graphs ):
        base_path = os.path.dirname(__file__)
        for graph in graphs.values():
            if graph.language == 'GLSL':
                graph.add_library( os.path.join( base_path, 'ShaderFunctions' ))
            if graph.language == 'Python':
                graph.add_library( os.path.join( base_path, 'PipelineNodes' ))

    @classmethod
    def blendermalt_register( self ):
        print( f'register {__package__}' )
        module_register( True, debug = False )
    
    @classmethod
    def blendermalt_unregister( self ):
        print( f'unregister {__package__}' )
        module_register( False, debug = False )
        import sys
        for submodule_name in [ x for x in sorted( sys.modules.keys( )) if x.startswith( __name__ )]:
            del sys.modules[ submodule_name ]

PLUGIN = ShadingEssentialsPlugin