
from pipeline_node import *

PREPASS_SHADER = None
BLUR_SHADER = None
COMBINE_SHADER = None

TEXTUREBLUR = generate_source('''
#include "Filters/Blur.glsl"

uniform sampler2D color_texture;
uniform float blur_radius = 7.0;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];
    
    // vec4 screen_color = box_blur( color_texture, uv, blur_radius, false );
    vec4 screen_color = gaussian_blur( color_texture, uv, blur_radius, 3.0 );
    
    RESULT = screen_color;
}
''')

PREPASS = generate_source('''

#include "Common/Color.glsl"

uniform sampler2D color_texture;
uniform float threshold = 0.35;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];
    
    vec4 color = texture( color_texture, uv );
    float luma = rgb_to_hsv( color.rgb ).z;

    color.rgb -= vec3( threshold );
    color = clamp( color, 0.0, 999.0 );

    RESULT = color;
}
''')

COMBINEPASS = generate_source('''

uniform sampler2D background;
uniform sampler2D blur_1;
uniform sampler2D blur_2;
uniform sampler2D blur_3;
uniform sampler2D blur_4;
uniform sampler2D blur_5;
uniform sampler2D blur_6;
uniform sampler2D blur_7;

uniform float intensity;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];

    vec4 back_color = texture( background, uv );
    sampler2D blur_images[7] = sampler2D[]( blur_1, blur_2, blur_3, blur_4, blur_5, blur_6, blur_7 );
    vec4 bloom;
    for( int i = 0; i < 7; ++i ){
        bloom.xyz += texture( blur_images[ i ], uv ).xyz * vec3( intensity );
    }
    
    RESULT = back_color + bloom;
}
''')

class EssentialsBloom( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Threshold' : ( 'float', 0.7 ),
            'Intensity' : ( 'float', 1.0 ),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
        }
    
    def get_render_targets(self, resolution: tuple[int, int]) -> dict[str, list[TextureTarget]]:
        return{
            'PREPASS' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F,  resolution )],
            'BLUR_1' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, scale_res( resolution, 1/2 ))],
            'BLUR_2' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, scale_res( resolution, 1/4 ))],
            'BLUR_3' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, scale_res( resolution, 1/8 ))],
            'BLUR_4' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, scale_res( resolution, 1/8 ))],
            'BLUR_5' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, scale_res( resolution, 1/16 ))],
            'BLUR_6' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, scale_res( resolution, 1/32 ))],
            'BLUR_7' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, scale_res( resolution, 1/64 ))],
            'COMBINE' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, resolution )],
        }
    
    def render( self, inputs: dict, outputs: dict ):
        
        global PREPASS_SHADER, BLUR_SHADER, COMBINE_SHADER
        if not PREPASS_SHADER:
            PREPASS_SHADER = self.compile_shader( PREPASS )
        if not BLUR_SHADER:
            BLUR_SHADER = self.compile_shader( TEXTUREBLUR )
        if not COMBINE_SHADER:
            COMBINE_SHADER = self.compile_shader( COMBINEPASS )
        
        if inputs[ 'Intensity' ] <= 0.0:
            outputs[ 'Color' ] = inputs[ 'Color' ]
            return
        
        #Prepass - Set the image to 0 at a certain threshold
        self.render_shader( PREPASS_SHADER, self.get_render_target( 'PREPASS' ),
            textures = { 'color_texture' : inputs[ 'Color' ]},
            uniforms = { 'threshold' : inputs[ 'Threshold' ]},
        )

        #First blur pass at 1/2 screen resolution
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_1' ),
            textures = { 'color_texture' : self.get_output( 'PREPASS', 'COLOR' )}
        )

        #Second blur pass at 1/4 screen resolution
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_2' ),
            textures = { 'color_texture' : self.get_output( 'BLUR_1', 'COLOR' )}
        )

        #Third blur pass at 1/4 screen resolution
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_3' ),
            textures = { 'color_texture' : self.get_output( 'BLUR_2', 'COLOR' )}
        )
        #Fourth blur pass at 1/8 screen resolution
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_4' ),
            textures = { 'color_texture' : self.get_output( 'BLUR_3', 'COLOR' )}
        )
        #Fifth blur pass at 1/16 screen resolution
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_5' ),
            textures = { 'color_texture' : self.get_output( 'BLUR_4', 'COLOR' )}
        )
        #Sixth blur pass at 1/32 screen resolution
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_6' ),
            textures = { 'color_texture' : self.get_output( 'BLUR_5', 'COLOR' )}
        )
        #Seventh blur pass at 1/64 screen resolution
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_7' ),
            textures = { 'color_texture' : self.get_output( 'BLUR_6', 'COLOR' )}
        )

        self.render_shader( COMBINE_SHADER, self.get_render_target( 'COMBINE' ),
            textures = {
                'background' : inputs[ 'Color' ],
                'blur_1' : self.get_output( 'BLUR_1', 'COLOR' ),
                'blur_2' : self.get_output( 'BLUR_2', 'COLOR' ),
                'blur_3' : self.get_output( 'BLUR_3', 'COLOR' ),
                'blur_4' : self.get_output( 'BLUR_4', 'COLOR' ),
                'blur_5' : self.get_output( 'BLUR_5', 'COLOR' ),
                'blur_6' : self.get_output( 'BLUR_6', 'COLOR' ),
                'blur_7' : self.get_output( 'BLUR_7', 'COLOR' ),
            },
            uniforms = {
                'intensity' : inputs[ 'Intensity' ]
            }
        )

        outputs[ 'Color' ] = self.get_output( 'COMBINE', 'COLOR' )



NODE = EssentialsBloom