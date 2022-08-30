from pipeline_node import *

PASSTHROUGH_SHADER = None
PASSTHROUGH_SOURCE = generate_source(
'''

#include "Filters/Blur.glsl"
#include "Filters/Kuwahara.glsl"
#include "Procedural/Noise.glsl"

uniform sampler2D tex;

layout (location=0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 c = UV[0] * 40.0;
    vec2 n = noise(vec4(c, 0.0, 0.0)).xy;
    n -= 0.5;
    n *= 100.0;
    RESULT = anisotropic_kuwahara(tex, UV[0], n, 2, 1000);
    // RESULT = vec4(n, 0.0, 1.0);
}

''')

class PassGate(CustomPipelineNode):

    is_rendered: bool = False

    def __init__(self, pipeline):
        super().__init__(pipeline)
        self.is_rendered = False

    @classmethod
    def static_inputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Texture': ('sampler2D', ''),
            'Update': ('bool', True)
        }
    
    @classmethod
    def static_outputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Texture': ('sampler2D', ''),
        }
    
    def get_render_targets(self, resolution: tuple[int, int], inputs) -> dict[str, list[TextureTarget]]:
        if inputs['Update'] or not 'Pass' in self.render_targets.keys():
            return {
                'Pass': [TextureTarget('MAIN', TextureFormat.RGBA32F, inputs['Texture'].resolution)]
            }
        else:
            return {}
    
    def render(self, inputs: dict, outputs: dict) -> None:
        global PASSTHROUGH_SHADER
        if not PASSTHROUGH_SHADER:
            PASSTHROUGH_SHADER = self.compile_shader(PASSTHROUGH_SOURCE)
        
        if inputs['Update'] or not self.is_rendered:
            self.render_shader(PASSTHROUGH_SHADER, self.get_render_target('Pass'),
                textures= {'tex': inputs['Texture']}
            )
            self.is_rendered = True
        
        outputs['Texture'] = self.get_output('Pass', 'MAIN')

NODE = PassGate
