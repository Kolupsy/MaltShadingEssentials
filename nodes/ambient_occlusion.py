from .utils import *

class MaltNodeAmbientOcclusion( EssentialsNode ):
    bl_idname = 'MaltNodeAmbientOcclusion'
    bl_label = 'Ambient Occlusion'
    menu_category = 'INPUT'

    def define_sockets( self ):
        return{
            'samples' : I( 'int', 'Samples', default = 32 ),
            'radius' : I( 'float', 'Radius', default = 1.0 ),
            'exponent' : I( 'float', 'Exponent', default = 1.0 ),
            'bias' : I( 'float', 'Bias', default = 0.01 ),
            'result' : O( 'float', 'Ambient Occlusion' )
        }
    
    def get_function( self ):
        f = '#ifdef NPR_FILTERS_ACTIVE\n'
        f += 'result = ao( samples, radius, exponent, bias );\n'
        f += '#else\n'
        f += '{result = 1.0;}\n'
        f += '#endif\n'
        return f
    
NODES = [ MaltNodeAmbientOcclusion ]