# from Malt.PipelineNode import PipelineNode
# from Malt.PipelineParameters import Parameter, Type
# from Malt.GL.Texture import Texture
# from Malt.GL.GL import GL_RGBA16F
# from Malt.GL.RenderTarget import RenderTarget
# from Malt.Render import Lighting

import pathlib
from pipeline_node import *

_SHADER = None

SHADERPATH = str( pathlib.Path( __file__ ).parent.parent.joinpath( 'Shaders', 'LensFlare.glsl' ))

# class EssentialsLensFlare( PipelineNode ):

#     def __init__( self, pipeline ):
#         PipelineNode.__init__( self, pipeline )
#         self.resolution = None
    
#     @classmethod
#     def reflect_inputs( cls ):
#         return {
#             'Color' : Parameter( '', Type.TEXTURE ),
#             'Depth' : Parameter( '', Type.TEXTURE ),
#             'Scene' : Parameter( 'Scene', Type.OTHER ),
#             'Sun Factor' : Parameter( 1.0, Type.FLOAT ),
#             'Point Factor' : Parameter( 0.1, Type.FLOAT ),
#             'Spot Factor' : Parameter( 0.1, Type.FLOAT ),
#             'Edge Fade' : Parameter( 5.0, Type.FLOAT ),
#         }
    
#     @classmethod
#     def reflect_outputs( cls ):
#         return {
#             'Color' : Parameter( '', Type.TEXTURE )
#         }
    
#     def setup_render_targets( self, resolution ):
#         self.resolution = resolution
#         self.texture_targets = {}
#         self.texture_targets[ 'COLOR' ] = Texture( resolution, GL_RGBA16F )
#         self.render_target = RenderTarget([*self.texture_targets.values( )])
    
#     def execute( self, parameters ):
#         inputs = parameters[ 'IN' ]
#         outputs = parameters[ 'OUT' ]

#         if self.pipeline.resolution != self.resolution:
#             self.setup_render_targets( self.pipeline.resolution )
        
#         global _SHADER
#         if _SHADER is None:
#             self.compile_shader( )
        
#         lights_buffer = Lighting.get_lights_buffer( )
#         lights_buffer.load( inputs[ 'Scene' ], 4, 0.9, 100.0, 1, 1.0 )
#         lights_buffer.shader_callback( _SHADER )

#         _SHADER.textures[ 'color_texture' ] = inputs[ 'Color' ]
#         _SHADER.textures[ 'depth_texture' ] = inputs[ 'Depth' ]
#         _SHADER.uniforms[ 'light_factors' ].set_value(( inputs[ 'Sun Factor' ], inputs[ 'Point Factor' ], inputs[ 'Spot Factor' ]))
#         _SHADER.uniforms[ 'edge_fade' ].set_value( inputs[ 'Edge Fade' ])
#         self.pipeline.common_buffer.shader_callback( _SHADER )
#         self.pipeline.draw_screen_pass( _SHADER, self.render_target )
            
#         outputs[ 'Color' ] = self.texture_targets[ 'COLOR' ]

#     def compile_shader_from_source( self, source, include_paths = [], defines = []):
#         return self.pipeline.compile_shader_from_source( source = source, include_paths = include_paths, defines = defines )

#     def compile_shader( self ):
#         global _SHADER
#         _SHADER = self.compile_shader_from_source( f'#include "{SHADERPATH}"' )

class EssentialsLensFlare( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Depth' : ( 'sampler2D', '' ),
            'Scene' : ( 'OTHER', 'Scene' ),
            'Sun Factor' : ( 'float', 1.0 ),
            'Point Factor' : ( 'float', 1.0 ),
            'Spot Factor' : ( 'float', 1.0 ),
            'Edge Fade' : ( 'float', 5.0 ),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' )
        }

    def get_render_targets( self, resolution: tuple[int, int]) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )]
        }
    
    
    def render( self, inputs: dict, outputs: dict ):
        
        global _SHADER
        if not _SHADER:
            _SHADER = self.compile_shader( f'#include "{SHADERPATH}"' )

        self.setup_lights_buffer( _SHADER, inputs[ 'Scene' ])
        
        self.render_shader( _SHADER, self.get_render_target( 'MAIN' ),
            textures = {
                'color_texture' : inputs[ 'Color' ],
                'depth_texture' : inputs[ 'Depth' ]
            },
            uniforms = {
                'light_factors' : ( inputs[ 'Sun Factor' ], inputs[ 'Point Factor' ], inputs[ 'Spot Factor' ]),
                'edge_fade' : inputs[ 'Edge Fade' ],
            }
        )
        outputs[ 'Color' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsLensFlare