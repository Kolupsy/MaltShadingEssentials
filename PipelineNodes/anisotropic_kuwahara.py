from pipeline_node import *

STRUCTURE_SHADER = None
STRUCTURE_SOURCE = generate_source('''

#include "Filters/StructureTensor.glsl"

uniform sampler2D tex;

layout (location = 0) out vec3 RESULT;

void main()
{
    PIXEL_SETUP_INPUT( );
    RESULT = structure_tensor(tex, UV[0]);
}
''')

DOWNSCALE_SHADER = None
DOWNSCALE_SOURCE = generate_source('''

#include "Filters/Blur.glsl"

uniform sampler2D tex;

layout (location = 0) out vec3 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();
    RESULT = box_blur(tex, UV[0], 3, true).xyz * 1.0;
}
''')

FILTER_SHADER = None
FILTER_SOURCE = generate_source('''

#include "Filters/Kuwahara.glsl"

uniform sampler2D tex;
uniform sampler2D tensor_tex;
uniform float anisotropy = 1.0;
uniform float size = 2.0;
uniform int samples = 100;

layout (location = 0) out vec4 OUT_COLOR;
layout (location = 1) out vec4 OUT_DEBUG;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 direction = texture(tensor_tex, UV[0]).gr * anisotropy;
    vec4 c = anisotropic_kuwahara(tex, UV[0], direction, size, samples);
    OUT_COLOR = c;
    OUT_DEBUG = vec4(direction, 0.0, 1.0);
}

''')

class AnisotropicKuwahara(CustomPipelineNode):
    
    @classmethod
    def static_inputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Color': ('sampler2D', ''),
            'Anisotropy': ('float', 1.0),
            'Size': ('float', 2.0),
            'Samples': ('int', 100),
        }    
    
    @classmethod
    def static_outputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Color': ('sampler2D', ''),
            'Debug': ('sampler2D', ''),
        }
    
    def get_render_targets(self, resolution: tuple[int, int], inputs) -> dict[str, list[TextureTarget]]:
        resolution = inputs['Color'].resolution
        return {
            'Structure': [TextureTarget('MAIN', TextureFormat.RGB16F, scale_res(resolution, 1/2))],
            'Downsample_1': [TextureTarget('MAIN', TextureFormat.RGB16F, scale_res(resolution, 1/2))],
            'Downsample_2': [TextureTarget('MAIN', TextureFormat.RGB16F, scale_res(resolution, 1/4))],
            'Filter': [
                TextureTarget('MAIN', TextureFormat.RGBA16F, resolution),
                TextureTarget('DEBUG', TextureFormat.RGBA16F, resolution)],
        }
    
    def render(self, inputs: dict, outputs: dict) -> None:
        
        global STRUCTURE_SHADER, DOWNSCALE_SHADER, FILTER_SHADER
        if not STRUCTURE_SHADER:
            STRUCTURE_SHADER = self.compile_shader(STRUCTURE_SOURCE)
        if not DOWNSCALE_SHADER:
            DOWNSCALE_SHADER = self.compile_shader(DOWNSCALE_SOURCE)
        if not FILTER_SHADER:
            FILTER_SHADER = self.compile_shader(FILTER_SOURCE)

        self.render_shader(STRUCTURE_SHADER, self.get_render_target('Structure'),
            textures = {'tex': inputs['Color']},
        )
        self.render_shader(DOWNSCALE_SHADER, self.get_render_target('Downsample_1'),
            textures = {'tex': self.get_output('Structure', 'MAIN')},
        )
        self.render_shader(DOWNSCALE_SHADER, self.get_render_target('Downsample_2'),
            textures = {'tex': self.get_output('Downsample_1', 'MAIN')},
        )
        self.render_shader(FILTER_SHADER, self.get_render_target('Filter'),
            textures = {
                'tex': inputs['Color'],
                'tensor_tex': self.get_output('Downsample_2', 'MAIN'),
                },
            uniforms = {
                'anisotropy': inputs['Anisotropy'],
                'size': inputs['Size'],
                'samples': inputs['Samples'],
            }
        )

        outputs['Color'] = self.get_output('Filter', 'MAIN')
        outputs['Debug'] = self.get_output('Filter', 'DEBUG')

NODE = AnisotropicKuwahara