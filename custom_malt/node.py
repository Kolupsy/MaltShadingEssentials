from BlenderMalt.MaltNodes.MaltNode import MaltNode

class MaltCustomNode( MaltNode ):
    bl_idname = 'MaltCustomNode'
    bl_label = 'Custom Malt Node'

    def setup( self ):
        super( ).setup( )
        
    def malt_init( self ):
        self.setup( )
    
    def update_tree( self ):
        self.id_data.update( )
    
    def get_source_socket_reference( self, socket ):
        transpiler = self.id_data.get_transpiler( )
        return transpiler.parameter_reference( self.get_source_name( ), socket.name, 'out' if socket.is_output else 'in' )
    
    def malt_setup( self ):
        if self.first_setup:
            self.name = self.bl_label
        self.setup_sockets( self.get_inputs( ), self.get_outputs( ))
    
    def get_inputs( self ) -> dict:
        return {}
    
    def get_outputs( self ) -> dict:
        return {}

    def get_source_code( self, transpiler ):
        return ''
    
    def set_defaults( self, **dictionary ):
        for key, value in dictionary.items( ):
            self.malt_parameters[ key ] = value
    
    def override_context( self, layout, operator_context = 'INVOKE_DEFAULT' ):
        layout.operator_context = operator_context
        layout.context_pointer_set( 'active_node', self )
    
    def draw_label( self ):
        return self.bl_label
    
    def update_socket_visibility( self ):
        pass