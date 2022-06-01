
class MaltVariable( ):
    name:str = ''
    type:str = 'float'
    min:float = None
    max:float = None
    default = None
    subtype = None

    def __init__( self, *args, min = None, max = None, default = None, subtype = None ):
        if len( args ) == 1:
            self.type = args[0]
        elif len( args ) == 2:
            self.type = args[0]
            self.name = args[1]
        else:
            print( 'Initialize MaltVariable with one or two arguments' )
        self.min = min
        self.max = max
        self.default = default
        self.subtype = subtype
    
    def get_init( self ):
        return f'{self.type} {self.name}'
    
    def get_dict( self ):
        d = {}
        d['type'] = self.type
        meta = {}
        for a in [ 'default', 'min', 'max', 'subtype' ]:
            value = getattr( self, a )
            if value:
                meta[a] = value
        d['meta'] = meta
        return d

class MaltVariableIn( MaltVariable ):
    is_out:bool = False

    def get_init( self ):
        return f'in {super( ).get_init( )}'

class MaltVariableOut( MaltVariable ):
    is_out:bool = True

    def get_init( self ):
        return f'out {super( ).get_init( )}'

class MaltFunction( ):

    body:str = ''
    name:str = ''
    inputs:dict = {}
    outputs:dict = {}

    @property
    def variables( self ):
        return { **self.inputs, **self.outputs }
    
    def __init__( self, body, name = '', **parameters ):
        if body.startswith( '\n' ):
            body = body[1:]
        if not body.endswith( '\n' ):
            body += '\n'
        self.body = body
        self.inputs, self.outputs = self.convert_parameters( **parameters )
        self.name = name
    
    def convert_parameters( self, **parameters ):
        inputs = {}
        outputs = {}
        for key, value in parameters.items( ):
            if not getattr( value, 'is_out' ):
                inputs[key] = value
            elif getattr( value, 'is_out' ):
                outputs[key] = value
            else:
                print( 'MaltFunction: MaltVariable needs to have attribute "is_out".')
        return inputs, outputs

    @property
    def function( self ):

        f = f'void {self.name}( '           # void some_name( 
        for name, type in self.inputs.items( ):
            f += f'{type} {name}, '         # void some_name( float fac, vec4 col, vec2 uv, 
        for name, type in self.outputs.items( ):
            f += f'out {type} {name}, '     # void some_name( float fac, vec4 col, vec2 uv, out vec4 result )
        f = f[:-2] + ' )\n{{\n'             # {{
        f += self.body
        f += '}}\n'
        return f