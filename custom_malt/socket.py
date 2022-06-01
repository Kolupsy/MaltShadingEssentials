from BlenderMalt.MaltNodes.MaltSocket import MaltSocket

class MaltSocketConvertible( MaltSocket ):
    bl_label = 'Convertible Malt Socket'

    def get_source_reference( self, target_type = None ):

        other_type = self.get_linked( ).data_type
        if other_type in [ 'vec2', 'vec3', 'vec4' ]:
            self.data_type = other_type
        super( ).get_source_reference( target_type = target_type )