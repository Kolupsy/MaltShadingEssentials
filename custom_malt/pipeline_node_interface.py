# import bpy
# from .node import MaltCustomNode
# from .pipeline_node import CustomPipelineNode

# class CustomPipelineInterface( bpy.types.Node, MaltCustomNode ):
#     bl_idname = 'CustomPipelineInterface'
#     bl_label = 'Custom Pipeline Interface'
#     pipeline_node:CustomPipelineNode = None

#     def get_inputs( self ) -> dict:
#         result = {}
#         for name, param in self.pipeline_node.reflect_inputs( ).items( ):
#             result[ name ] = { 'type' : param }
#         return result
#     def get_outputs( self ) -> dict:
#         result = {}
#         for name, param in self.pipeline_node.reflect_outputs( ).items( ):
#             result[ name ] = { 'type' : param }
#         return result
