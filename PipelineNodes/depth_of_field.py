from pipeline_node import *

# Based on: https://catlikecoding.com/unity/tutorials/advanced-rendering/depth-of-field/

COC_SHADER = None
COC_SOURCE = generate_source('''

#include "Common/Transform.glsl"

uniform sampler2D depth_texture;
uniform float focus_distance = 10.0;
uniform float focus_range = 3.0;
uniform float bokeh_radius = 4.0;

layout (location = 0) out float COC;

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 depth_alpha = texture( depth_texture, UV[0]).xw;

    COC = ( depth_alpha.x - focus_distance ) / focus_range;
    COC = clamp( COC, -1, 1 ) * bokeh_radius;
    COC = mix( bokeh_radius, COC, depth_alpha.y );
}
''')

PREFILTER_SHADER = None
PREFILTER_SOURCE = generate_source('''

uniform sampler2D color_texture;
uniform sampler2D coc_texture;

layout (location = 0) out vec4 OUT_COLOR;

float avg_weight( vec3 c ){
    return 1 / ( 1 + max( max( c.r, c.g ), c.b ));
}

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 texel = vec2( 1.0 ) / vec2( textureSize( color_texture, 0 ));
    vec4 offset = texel.xyxy * vec2( -0.5, 0.5 ).xxyy;

    vec3 s0 = texture( color_texture, UV[0] + offset.xy ).rgb;
    float w0 = avg_weight( s0 );
    vec3 s1 = texture( color_texture, UV[0] + offset.zy ).rgb;
    float w1 = avg_weight( s1 );
    vec3 s2 = texture( color_texture, UV[0] + offset.xw ).rgb;
    float w2 = avg_weight( s2 );
    vec3 s3 = texture( color_texture, UV[0] + offset.zw ).rgb;
    float w3 = avg_weight( s3 );

    vec3 color = s0 * w0 + s1 * w1 + s2 * w2 + s3 * w3;
    color /= max( 0.000001, w0 + w1 + w2 + w3 );

    float coc0 = texture( coc_texture, UV[0] + offset.xy ).x;
    float coc1 = texture( coc_texture, UV[0] + offset.zy ).x;
    float coc2 = texture( coc_texture, UV[0] + offset.xw ).x;
    float coc3 = texture( coc_texture, UV[0] + offset.zw ).x;
    float coc = ( coc0 + coc1 + coc2 + coc3 ) * 0.25;
    OUT_COLOR = vec4( color, coc );
}
''')

BOKEH_SHADER = None
BOKEH_SOURCE = generate_source('''

#include "Node Utils/common.glsl"

uniform sampler2D color_texture;
uniform float bokeh_radius = 4.0;

layout (location = 0) out vec4 BOKEH;
layout (location = 1) out float OUT_COC;

float coc_weight( float coc, float radius ){
    return clamp(( coc - radius + 2 ) / 2, 0.0, 1.0 );
}

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 texel = vec2( 1.0 ) / textureSize( color_texture, 0 );

    int kernel_samples = 22;
    vec2 kernel[] = vec2[]( 
        vec2(0, 0),
        vec2(0.53333336, 0),
        vec2(0.3325279, 0.4169768),
        vec2(-0.11867785, 0.5199616),
        vec2(-0.48051673, 0.2314047),
        vec2(-0.48051673, -0.23140468),
        vec2(-0.11867763, -0.51996166),
        vec2(0.33252785, -0.4169769),
        vec2(1, 0),
        vec2(0.90096885, 0.43388376),
        vec2(0.6234898, 0.7818315),
        vec2(0.22252098, 0.9749279),
        vec2(-0.22252095, 0.9749279),
        vec2(-0.62349, 0.7818314),
        vec2(-0.90096885, 0.43388382),
        vec2(-1, 0),
        vec2(-0.90096885, -0.43388376),
        vec2(-0.6234896, -0.7818316),
        vec2(-0.22252055, -0.974928),
        vec2(0.2225215, -0.9749278),
        vec2(0.6234897, -0.7818316),
        vec2(0.90096885, -0.43388376)
        );
    
    float current_coc = texture( color_texture, UV[0]).a;

    vec3 bg_color, fg_color;
    float bg_weight, fg_weight;
    for( int k = 0; k < kernel_samples; ++k ){
        vec2 offset = kernel[k] * vec2( bokeh_radius );
        float radius = length( offset );
        offset *= texel;

        vec4 new_color = texture( color_texture, UV[0] + offset );

        float bgw = coc_weight( max( 0, min( new_color.a, current_coc )), radius );
        bg_color += new_color.rgb * vec3( bgw );
        bg_weight += bgw;

        float fgw = coc_weight( - new_color.a, radius );
        fg_color += new_color.rgb * vec3( fgw );
        fg_weight += fgw;

    }
    bg_color /= vec3( max( bg_weight, 0.000001 ));
    fg_color /= vec3( max( fg_weight, 0.000001 ));
    float fg_bg_mix = min( 1, fg_weight * PI / kernel_samples );
    vec3 color = mix( bg_color, fg_color, fg_bg_mix );
    BOKEH = vec4( color, fg_bg_mix );
    OUT_COC = current_coc;
}
''')

BOKEH_SOURCE_ALT = generate_source('''

#include "Node Utils/common.glsl"

uniform sampler2D color_texture;
uniform float bokeh_radius = 4.0;
uniform int kernel_samples = 22;
uniform float GOLDEN_ANGLE = 2.3998;

layout (location = 0) out vec4 BOKEH;
layout (location = 1) out float OUT_COC;

float coc_weight( float coc, float radius ){
    return clamp(( coc - radius + 2 ) / 2, 0.0, 1.0 );
}

mat2 rot_mat = mat2(
    cos( GOLDEN_ANGLE ), sin( GOLDEN_ANGLE ),
    -sin( GOLDEN_ANGLE ), cos( GOLDEN_ANGLE )
);

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 texel = vec2( 1.0 ) / textureSize( color_texture, 0 );
    
    float current_coc = texture( color_texture, UV[0]).a;
    vec3 bg_color, fg_color;
    float bg_weight, fg_weight;

    for( int k = 0; k < kernel_samples; ++k ){

        float r = float( k ) * GOLDEN_ANGLE;
        vec2 offset = vec2( cos( r ), sin( r )) * vec2( pow( float( k ) / kernel_samples, 0.5 ));
        offset *= vec2( bokeh_radius );
        float radius = length( offset );
        offset *= texel;

        vec4 new_color = texture( color_texture, UV[0] + offset );

        float bgw = coc_weight( max( 0, min( new_color.a, current_coc )), radius );
        bg_color += new_color.rgb * vec3( bgw );
        bg_weight += bgw;

        float fgw = coc_weight( - new_color.a, radius );
        fg_color += new_color.rgb * vec3( fgw );
        fg_weight += fgw;

    }
    bg_color /= vec3( max( bg_weight, 0.000001 ));
    fg_color /= vec3( max( fg_weight, 0.000001 ));
    float fg_bg_mix = min( 1, fg_weight * PI / kernel_samples );
    vec3 color = mix( bg_color, fg_color, fg_bg_mix );
    BOKEH = vec4( color, fg_bg_mix );
    OUT_COC = current_coc;
}
''')

TENT_SHADER = None
TENT_SOURCE = generate_source('''

uniform sampler2D tex;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 texel = vec2( 1.0 ) / textureSize( tex, 0 );
    vec4 offset = texel.xyxy * vec2( -0.5, 0.5 ).xxyy;

    RESULT =
        texture( tex, UV[0] + offset.xy ) +
        texture( tex, UV[0] + offset.zy ) +
        texture( tex, UV[0] + offset.xw ) +
        texture( tex, UV[0] + offset.zw );
    RESULT *= vec4( 0.25 );
}
''')

COMBINE_SHADER = None
COMBINE_SOURCE = generate_source('''

uniform sampler2D original;
uniform sampler2D dof_texture;
uniform sampler2D coc_texture;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT( );

    vec4 source = texture( original, UV[0]);
    vec4 dof = texture( dof_texture, UV[0]);
    float bgfg = dof.a;
    float coc = texture( coc_texture, UV[0]).x;

    float dof_strength = smoothstep( 0.1, 1.0, abs( coc ));
    vec3 color = mix( 
        source.rgb, 
        dof.rgb, 
        dof_strength + bgfg - dof_strength * bgfg
        );

    RESULT = vec4( color, 1.0 );
    // RESULT = vec4( vec3( coc ), 1.0 );
}
''')

class EssentialsDOF( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Depth' : ( 'sampler2D', '' ),
            'Focus Distance' : ( 'float', 5.0 ),
            'Focus Range' : ( 'float', 10.0 ),
            'Bokeh Radius' : ( 'float', 10.0 ),
            'Samples' : ( 'int', 150 ),
        }
    
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' )
        }
    
    def get_render_targets( self, resolution: tuple[int, int], inputs) -> dict[str, list[TextureTarget]]:
        return {
            'COC' : [ TextureTarget( 'Main', TextureFormat.R16F, resolution )],
            'COLOR_COC' : [ TextureTarget( 'Color', TextureFormat.RGBA32F, scale_res( resolution, 1/2 ))],
            'BOKEH' : [ 
                TextureTarget( 'Color', TextureFormat.RGBA16F, scale_res( resolution, 1/2 )),
                TextureTarget( 'COC', TextureFormat.R16F, scale_res( resolution, 1/2 )),
                ],
            'TENT' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, scale_res( resolution, 1/2 ))],
            'COMBINE' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, resolution )],
        }
    
    def render( self, inputs: dict, outputs: dict ) -> None:
        
        global COC_SHADER, PREFILTER_SHADER, BOKEH_SHADER, TENT_SHADER, COMBINE_SHADER
        if not COC_SHADER:
            COC_SHADER = self.compile_shader( COC_SOURCE )
        if not PREFILTER_SHADER:
            PREFILTER_SHADER = self.compile_shader( PREFILTER_SOURCE )
        if not BOKEH_SHADER:
            BOKEH_SHADER = self.compile_shader( BOKEH_SOURCE_ALT )
        if not TENT_SHADER:
            TENT_SHADER = self.compile_shader( TENT_SOURCE )
        if not COMBINE_SHADER:
            COMBINE_SHADER = self.compile_shader( COMBINE_SOURCE )

        if inputs[ 'Samples' ] <= 1 or inputs[ 'Bokeh Radius'] <= 0:
            outputs[ 'Color' ] = inputs[ 'Color' ]
            return

        #Setting up the Circle of Confusion texture
        self.render_shader( COC_SHADER, self.get_render_target( 'COC' ),
            textures = { 'depth_texture' : inputs[ 'Depth' ]},
            uniforms = {
                'focus_distance' : inputs[ 'Focus Distance' ],
                'focus_range' : inputs[ 'Focus Range' ],
                'bokeh_radius' : inputs[ 'Bokeh Radius' ],
            }
        )
        #Combining the scene color with the COC texture at 1/2 res
        self.render_shader( PREFILTER_SHADER, self.get_render_target( 'COLOR_COC' ),
            textures = {
                'color_texture' : inputs[ 'Color' ],
                'coc_texture' : self.get_output( 'COC', 'Main' ),
            }
        )
        #Generating the DOF (main part) with COC data at 1/2 res
        self.render_shader( BOKEH_SHADER, self.get_render_target( 'BOKEH' ),
            textures = { 
                'color_texture' : self.get_output( 'COLOR_COC', 'Color' )
                },
            uniforms = { 
                'bokeh_radius' : inputs[ 'Bokeh Radius' ],
                'kernel_samples' : inputs[ 'Samples' ],
                },
        )
        #Blur the DOF texture to get a smoother look
        self.render_shader( TENT_SHADER, self.get_render_target( 'TENT' ),
            textures = { 'tex' : self.get_output( 'BOKEH', 'Color' )}
        )
        self.render_shader( COMBINE_SHADER, self.get_render_target( 'COMBINE' ),
            textures = { 
                'original' : inputs[ 'Color' ],
                'dof_texture' : self.get_output( 'TENT', 'Main' ),
                'coc_texture' : self.get_output( 'BOKEH', 'COC' ),
                }
        )

        outputs[ 'Color' ] = self.get_output( 'COMBINE', 'Main' )

NODE = EssentialsDOF