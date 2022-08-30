from pipeline_node import *

STRUCTURE_SHADER = None
STRUCTURE_SOURCE = generate_source(
'''

#include "Filters/StructureTensor.glsl"

uniform sampler2D tex;

layout (location=0) out vec3 STRUCTURE;

void main()
{
    PIXEL_SETUP_INPUT();
    STRUCTURE = structure_tensor(tex, UV[0]);
}

''')

BLUR_SHADER = None
BLUR_SOURCE = generate_source(
'''

uniform sampler2D tex;
uniform vec2 direction;

layout (location=0) out vec3 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();

    vec2 texel_offset = direction * (1.0 / textureSize(tex, 0));

    vec3 gaussian_kernel[4] = vec3[]
    (
        vec3( texel_offset * -2.0, 1.0/16.0),
        vec3( texel_offset * -1.0, 4.0/16.0),
        vec3( texel_offset * +1.0, 4.0/16.0),
        vec3( texel_offset * +2.0, 1.0/16.0)
    );

    vec3 result = texture(tex, UV[0]).xyz * (6.0 / 16.0);

    for(int i = 0; i < 4; i++)
    {
        vec3 kd = gaussian_kernel[i];
        result += texture(tex, UV[0] + kd.xy).xyz * kd.z;
    }

    RESULT = result;
}

''')

FILTER_SHADER = None
FILTER_SOURCE = generate_source(
'''

#include "Filters/Blur.glsl"
#include "Filters/StructureTensor.glsl"

uniform sampler2D color_tex;
uniform sampler2D structure_tex;

uniform float sigma_d = 6.0;
uniform float sigma_r = 0.55;

layout(location=0) out vec4 OUT_COLOR;

void main()
{
    PIXEL_SETUP_INPUT();   
    vec3 flow_field = flow_from_structure(texture(structure_tex, UV[0]).rgb);
    OUT_COLOR = OAB_blur(color_tex, UV[0], flow_field.xy, sigma_d, sigma_r);
}
''')

class OrientationAlignedBilateralBlur(CustomPipelineNode):

    @classmethod
    def static_inputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Color': ('sampler2D', ''),
            'Radius': ('float', 6.0),
            'Smoothness': ('float', 0.55),
        }
    
    @classmethod
    def static_outputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Color': ('sampler2D', ''),
        }
    
    def get_render_targets(self, resolution: tuple[int, int], inputs) -> dict[str, list[TextureTarget]]:
        resolution = inputs['Color'].resolution
        return {
            'Structure': [TextureTarget('MAIN', TextureFormat.RGB16F, resolution)],
            'Blur': [TextureTarget('MAIN', TextureFormat.RGB16F, resolution)],
            'Filter': [TextureTarget('MAIN', TextureFormat.RGBA16F, resolution)]
        }
    
    def render(self, inputs: dict, outputs: dict) -> None:
        global STRUCTURE_SHADER, BLUR_SHADER, FILTER_SHADER
        if not STRUCTURE_SHADER:
            STRUCTURE_SHADER = self.compile_shader(STRUCTURE_SOURCE)
        if not BLUR_SHADER:
            BLUR_SHADER = self.compile_shader(BLUR_SOURCE)
        if not FILTER_SHADER:
            FILTER_SHADER = self.compile_shader(FILTER_SOURCE)


        self.render_shader(STRUCTURE_SHADER, self.get_render_target('Structure'),
            textures={'tex': inputs['Color']},
        )
        self.render_shader(BLUR_SHADER, self.get_render_target('Blur'),
            textures={'tex': self.get_output('Structure', 'MAIN')},
            uniforms={'direction': (1.0,0.0)}
        )
        self.render_shader(BLUR_SHADER, self.get_render_target('Structure'),
            textures={'tex': self.get_output('Blur', 'MAIN')},
            uniforms={'direction': (0.0, 1.0)}
        )
        self.render_shader(FILTER_SHADER, self.get_render_target('Filter'),
            textures={
                'color_tex': inputs['Color'],
                'structure_tex': self.get_output('Structure', 'MAIN')},
            uniforms={
                'sigma_d': inputs['Radius'],
                'sigma_r': inputs['Smoothness'],
            }
        )

        outputs['Color'] = self.get_output('Filter', 'MAIN')

NODE = OrientationAlignedBilateralBlur
