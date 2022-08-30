from pipeline_node import *

CLOUD_SHADER = None
CLOUD_SOURCE = generate_source(
'''

#include "Procedural/Fractal_Noise.glsl"
#include "Procedural/Cell_Noise.glsl"

vec4 Noise2D(vec2 uv, float scale, float detail, float balance)
{
    vec4 c = vec4(uv, TIME * 0.001, 0.0);
    c *= scale;
    return fractal_noise_ex(c, detail, balance, true, vec4(scale));
}

vec2 NoiseDistort(vec2 uv, float scale, float detail, float balance, float distortion)
{
    if(distortion <= 0.0)
    {
        return vec2(0.0);
    }
    vec2 d = Noise2D(uv, scale, detail, balance).xy;
    d -= 0.5;
    return d * distortion;
}

float Cell2D(vec2 uv, float scale)
{
    vec4 c = vec4(uv, TIME * 0.01, 0.0);
    c *= scale;
    CellNoiseResult r = cell_noise_ex(c, true, vec4(scale));
    return r.cell_distance;
}

layout (location=0) out vec4 CLOUD_MASK;

void main()
{
    PIXEL_SETUP_INPUT();

    vec2 uv = UV[0] + vec2(TIME * 0.01, 0.0);

    float main_chunks = Cell2D(uv + NoiseDistort(uv, 5, 3, 0.3, 0.1), 5);
    float sec_chunks = Cell2D(uv + NoiseDistort(uv, 25, 3, 0.3, 0.08), 10);
    float small_chunks = Cell2D(uv + NoiseDistort(uv, 100, 2, 0.5, 0.02), 50);


    float clouds = mix(main_chunks, sec_chunks, 0.5);
    clouds = mix(clouds, small_chunks, 0.1);
    clouds = saturate(map_range(clouds, 0.2, 0.55, 1.0, 0.0));
    clouds = smoothstep(0.0, 1.0, clouds);

    CLOUD_MASK = vec4(vec3(clouds), 1.0);
}

''')

class EssentialsClouds( CustomPipelineNode ):

    @classmethod
    def static_inputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Main Clouds' : ( 'float', 0.65 ),
            'Streaky Clouds' : ( 'float', 0.3 ),
            'Wind Speed' : ( 'float', 0.05 ),
            'Wind Angle' : ( 'float', 0.0 ),
        }
    @classmethod
    def static_outputs( cls ) -> dict[tuple[str, Any]]:
        return{
            'Clouds' : ( 'sampler2D', '' )
        }
    
    def get_render_targets( self, resolution: tuple[int, int], inputs) -> dict[str, TextureTarget]:
        return {
            'MAIN' : [ TextureTarget( 'COLOR', TextureFormat.RGBA16F, (1024, 1024))]
        }
    
    
    def render( self, inputs: dict, outputs: dict ):
        
        global CLOUD_SHADER
        if not CLOUD_SHADER:
            CLOUD_SHADER = self.compile_shader(CLOUD_SOURCE)
        
        self.render_shader(CLOUD_SHADER, self.get_render_target('MAIN'),
        
        )
        outputs[ 'Clouds' ] = self.get_output( 'MAIN', 'COLOR' )

NODE = EssentialsClouds