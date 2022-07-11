from pipeline_node import *

DISTORTION_SHADER = None
DISTORTION_SOURCE = generate_source('''

vec2 distorted_UVs( vec2 uv, float k, float kcube ){
    
    vec2 t = uv - 0.5;
    float r2 = t.x * t.x + t.y * t.y;
	float f = 0.0;
    
    if( kcube == 0.0 ){
        f = 1.0 + r2 * k;
    }else{
        f = 1.0 + r2 * ( k + kcube * sqrt( r2 ) );
    }
    return f * t + 0.5;
}

vec4 distorted_channel( sampler2D tex, vec2 uv, float k, float kcube, float offset, float blur, int channel ){
    float offset_k = k;
    if( channel == 0 ){
        offset_k = k + offset;
    }
    if( channel == 2 ){
        offset_k = k - offset;
    }

    vec2 nUv = distorted_UVs( uv, offset_k, kcube );
    vec2 c = abs( nUv - 0.5 );
    vec4 result = texture( tex, nUv ).rgba;
    if( max( c.x, c.y ) > 0.5 ){
        result = vec4( 0.0, 0.0, 0.0, result.a );
    }
    
    return result;
}

uniform sampler2D color_texture;
uniform float distortion = -0.1;
uniform float dispersion = 1.0;

layout (location = 0) out vec4 OUT_COLOR;
layout (location = 1) out float OUT_GRADIENT;

void main()
{
    PIXEL_SETUP_INPUT( );
    vec2 uv = UV[0];

    float k = distortion * 0.9;
    float kcube = 0.5 * distortion;
    float offset = dispersion * distortion * 0.5;
    float red = distorted_channel( color_texture, uv, k, kcube, offset, 0.0, 0 ).r;
    float green = distorted_channel( color_texture, uv, k, kcube, offset, 0.0, 1 ).g;
    float blue = distorted_channel( color_texture, uv, k, kcube, offset, 0.0, 2 ).b;

    float gradient = length( distorted_UVs( uv, k, kcube ) - 0.5);
    gradient = smoothstep( 0.0, 1.0, gradient );
    
    OUT_COLOR = vec4( red, green, blue, 1.0 );
    OUT_GRADIENT = gradient;
}
''')

BLUR_SHADER = None
BLUR_SOURCE = generate_source('''

uniform sampler2D color_texture;
uniform sampler2D gradient_texture;
uniform vec2 blur_vector = vec2( 0.0, 0.1 );

layout (location = 0) out vec4 OUT_COLOR;

void main()
{
    PIXEL_SETUP_INPUT( );

    vec4 result;
    float total;
    float radius_multiplier = texture( gradient_texture, UV[0] ).r;
    vec2 bv = blur_vector * radius_multiplier;
    float radius = length( bv * vec2( textureSize( color_texture, 0 )));
    
    for( float a = -radius; a <= radius; a++ ){

        vec2 offset = bv * vec2( a / radius );
        float w = 1 - abs( a / radius );
        result += texture( color_texture, UV[0] + offset ) * w;
        total += w;
    }
    result /= total;

    OUT_COLOR = result;
}
''')

class EssentialsLensDistortion( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
            'Distortion' : ( 'float', -0.1 ),
            'Dispersion' : ( 'float', 1.0 ),
            'Blur' : ( 'float', 0.1 ),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Color' : ( 'sampler2D', '' ),
        }
    
    def get_render_targets( self, resolution: tuple[int, int]) -> dict[str, TextureTarget]:
        return {
            'DISTORT' : [ 
                TextureTarget( 'Main', TextureFormat.RGBA16F, resolution ),
                TextureTarget( 'Gradient', TextureFormat.R16F, resolution ),
            ],
            'BLUR_1' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, resolution )],
            'BLUR_2' : [ TextureTarget( 'Main', TextureFormat.RGBA16F, resolution )],
        }
    
    def render( self, inputs: dict, outputs: dict ):
        
        global DISTORTION_SHADER, BLUR_SHADER
        if not DISTORTION_SHADER:
            DISTORTION_SHADER = self.compile_shader( DISTORTION_SOURCE )
        if not BLUR_SHADER:
            BLUR_SHADER = self.compile_shader( BLUR_SOURCE )
        
        self.render_shader( DISTORTION_SHADER, self.get_render_target( 'DISTORT' ),
            textures = { 'color_texture' : inputs[ 'Color' ] },
            uniforms = {
                'distortion' : inputs[ 'Distortion' ],
                'dispersion' : inputs[ 'Dispersion' ],
            }
        )

        blur = inputs[ 'Blur' ]
        if blur <= 0.0:
            outputs[ 'Color' ] = self.get_output( 'DISTORT', 'Main' )
            return

        #vertical blur pass
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_1' ),
            textures = { 
                'color_texture' : self.get_output( 'DISTORT', 'Main' ),
                'gradient_texture' : self.get_output( 'DISTORT', 'Gradient' ),
                },
            uniforms = { 'blur_vector' : ( 0.0, blur)},
        )

        #horizontal blur pass
        self.render_shader( BLUR_SHADER, self.get_render_target( 'BLUR_2' ),
            textures = { 
                'color_texture' : self.get_output( 'BLUR_1', 'Main' ),
                'gradient_texture' : self.get_output( 'DISTORT', 'Gradient' ),
                },
            uniforms = { 'blur_vector' : ( blur, 0.0 )},
        )

        outputs[ 'Color' ] = self.get_output( 'BLUR_2', 'Main' )

NODE = EssentialsLensDistortion