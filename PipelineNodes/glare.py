from pipeline_node import *
import math

LIMIT_SHADER = None
LIMIT_SOURCE = generate_source('''

uniform sampler2D color_texture;
uniform float threshold = 0.0;

layout (location = 0) out vec4 OUT_COLOR;

void main()
{
    PIXEL_SETUP_INPUT( );

    vec4 color = texture( color_texture, UV[0] );
    color.rgb -= threshold;
    color.rgb = clamp( color.rgb, 0.0, 1.0 );

    OUT_COLOR = color;
}

''')

BLUR_DIR_SHADER = None
BLUR_DIR_SOURCE = generate_source('''

#include "Node Utils/common.glsl"

uniform sampler2D previous_texture;
uniform sampler2D limit_texture;
uniform vec2 blur_direction = vec2( 0.1, 0.0 );
uniform float glare_focus = 3.0;
uniform float glare_influence = 1.0;

layout (location = 0) out vec4 OUT_COLOR;

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 res = render_resolution( );
    vec2 direction = blur_direction * vec2( 1, res.x / res.y );

    float radius = length( direction * res );
    radius = min( radius, 1000 );
    vec4 result;
    float total_weight;
    float max_value;
    for( float i = -radius; i <= radius; i++ ){
        float rat = i / radius;
        float s = 1 - abs( rat );
        s = pow( s, glare_focus );
        total_weight += s;
        if( s <= 0.0 ){
            continue;
        }
        vec2 offset = direction * rat;
        vec4 new_sample = texture( limit_texture, UV[0] + offset );
        max_value = max( max_value, length( new_sample ));
        result += new_sample * pow( s * 2, 2 );
    }
    result /= total_weight;
    result = max( vec4( 0.0 ), result );

    vec4 new_color = texture( previous_texture, UV[0]);
    new_color.rgb += result.rgb * glare_influence;

    OUT_COLOR = new_color;
}
''')

COMBINE_SHADER = None
COMBINE_SOURCE = generate_source('''

uniform sampler2D original_texture;
uniform sampler2D glare_texture;
uniform float glare_influence = 1.0;

layout (location = 0) out vec4 OUT_COLOR;

void main()
{
    PIXEL_SETUP_INPUT( );

    vec4 original_color = texture( original_texture, UV[0] );
    vec4 glare_color = texture( glare_texture, UV[0] );
    glare_color = max( vec4( 0.0 ), glare_color );
    vec4 result = original_color;
    result.rgb += glare_color.rgb * glare_influence;

    OUT_COLOR = result;
}

''')

class EssentialsGlare( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Streaks' : ( 'int', 2 ),
            'Threshold' : ( 'float', 0.5 ),
            'Glare Size' : ( 'float', 0.05 ),
            'Angle' : ( 'float', 0.0 ),
            'Focus' : ( 'float', 3.0 ),
            'Strength' : ( 'float', 1.0 ),
        }
    
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
        }
    
    def get_render_targets( self, resolution: tuple[int, int]) -> dict[str, list[TextureTarget]]:
        return{
            'LIMIT' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, scale_res( resolution, 1 ))],
            'BLUR_1' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, resolution )],
            'BLUR_2' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, resolution )],
            'COMBINE' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, resolution )],
        }
    
    def render( self, inputs: dict, outputs: dict ) -> None:
        
        global LIMIT_SHADER, BLUR_DIR_SHADER, COMBINE_SHADER
        if not LIMIT_SHADER:
            LIMIT_SHADER = self.compile_shader( LIMIT_SOURCE )
        if not BLUR_DIR_SHADER:
            BLUR_DIR_SHADER = self.compile_shader( BLUR_DIR_SOURCE )
        if not COMBINE_SHADER:
            COMBINE_SHADER = self.compile_shader( COMBINE_SOURCE )
        
        color_input = inputs[ 'Color' ]
        glare_threshold = inputs[ 'Threshold' ]
        glare_size = inputs[ 'Glare Size' ]
        
        #limits the influence of the glare using a threshold
        self.render_shader( LIMIT_SHADER, self.get_render_target( 'LIMIT' ),
            textures = {
                'color_texture' : color_input
            },
            uniforms = {
                'threshold' : glare_threshold,
            },
        )
        
        streak_count = inputs[ 'Streaks' ]
        for i in range( streak_count ):
            
            ratio = i / inputs[ 'Streaks' ] + inputs[ 'Angle' ]
            direction = ( math.cos( ratio * math.pi ) * glare_size, math.sin( ratio * math.pi ) * glare_size )

            from_tex = self.get_output( 'BLUR_2', 'Main' ) if i % 2 == 0 else self.get_output( 'BLUR_1', 'Main' )
            if i == 0:
                from_tex = color_input
            to_pass_name = 'BLUR_1' if i % 2 == 0 else 'BLUR_2'

            self.render_shader( BLUR_DIR_SHADER, self.get_render_target( to_pass_name ),
                textures = {
                    'previous_texture' : from_tex,
                    'limit_texture' : self.get_output( 'LIMIT', 'Main' )
                },
                uniforms = {
                    'blur_direction' : direction,
                    'glare_focus' : inputs[ 'Focus' ],
                    'glare_influence' : inputs[ 'Strength' ]
                }
            )

        outputs[ 'Color' ] = self.get_output( to_pass_name, 'Main' )

NODE = EssentialsGlare