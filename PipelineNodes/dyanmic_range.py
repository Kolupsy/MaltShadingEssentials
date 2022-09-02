from pipeline_node import *

DR_SHADER = None
DR_SOURCE = generate_source(
"""
#include "Common/Color.glsl"

uniform sampler2D tex;
uniform bool is_init = false;

layout (location = 0) out float RESULT;

void main()
{
    PIXEL_SETUP_INPUT();
    RESULT = 0.0;
    vec2 texel = 1.0 / textureSize(tex, 0);

    int radius = 2;

    for(int u=-radius; u <= radius; u++)
    {
        for(int v =-radius; v <= radius; v++)
        {
            vec2 offset = vec2(u,v) * texel;
            float l;
            if(is_init)
            {
                l = luma(texture(tex, UV[0] + offset).rgb);
            }
            else
            {
                l = texture(tex, UV[0] + offset).x;
            }
            RESULT += l;
        }
    }
    RESULT /= pow(2 * float(radius) + 1.0, 2);
}
""")

COMP_SHADER = None
COMP_SOURCE = generate_source(
"""

uniform sampler2D color_tex;
uniform sampler2D dr_tex;
uniform float auto_exposure = 1.0;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT();

    ivec2 dr_resolution = textureSize(dr_tex, 0);
    vec2 dr_texel = 1.0 / vec2(dr_resolution);
    float brightness = 0.0;

    for(int u=0; u < dr_resolution.x; u++)
    {
        for(int v=0; v < dr_resolution.y; v++)
        {
            vec2 offset = vec2(u,v) * dr_texel;
            float s = texture(dr_tex, offset).x;
            brightness += s;
        }
    }
    float avg_brightness = brightness / dr_resolution.x / dr_resolution.y;
    vec4 color = texture(color_tex, UV[0]);
    color.rgb /= 2 * mix(0.5, avg_brightness, saturate(auto_exposure));
    RESULT = color;
}

""")

class ToneMapper(CustomPipelineNode):

    @classmethod
    def static_inputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Color': ('sampler2D', ''),
            'Auto Exposure': ('float', 1.0),
        }
    
    @classmethod
    def static_outputs(cls) -> dict[tuple[str, Any]]:
        return {
            'Color': ('sampler2D', '')
        }
    
    def get_render_targets(self, resolution: tuple[int, int], inputs) -> dict[str, list[TextureTarget]]:
        return {
            'DR_1': [TextureTarget('MAIN', TextureFormat.R16F, resolution)],
            'DR_2': [TextureTarget('MAIN', TextureFormat.R16F, scale_res(resolution, 1/4))],
            'DR_3': [TextureTarget('MAIN', TextureFormat.R16F, scale_res(resolution, 1/16))],
            'DR_4': [TextureTarget('MAIN', TextureFormat.R16F, scale_res(resolution, 1/64))],
            'Comp': [TextureTarget('MAIN', TextureFormat.RGBA16F, resolution)],
        }

    def render(self, inputs: dict, outputs: dict) -> None:
        global DR_SHADER, COMP_SHADER
        if not DR_SHADER:
            DR_SHADER = self.compile_shader(DR_SOURCE)
        if not COMP_SHADER:
            COMP_SHADER = self.compile_shader(COMP_SOURCE)
        
        if inputs['Auto Exposure'] <= 0.0:
            outputs['Color'] = inputs['Color']
            return
        
        self.render_shader(DR_SHADER, self.get_render_target('DR_1'),
            textures= {'tex': inputs['Color']},
            uniforms= {'is_init': True}
        )
        self.render_shader(DR_SHADER, self.get_render_target('DR_2'),
            textures= {'tex': self.get_output('DR_1', 'MAIN')},
            uniforms= {'is_init': False}
        )
        self.render_shader(DR_SHADER, self.get_render_target('DR_3'),
            textures= {'tex': self.get_output('DR_2', 'MAIN')},
            uniforms= {'is_init': False}
        )
        self.render_shader(DR_SHADER, self.get_render_target('DR_4'),
            textures= {'tex': self.get_output('DR_3', 'MAIN')},
            uniforms= {'is_init': False}
        )
        self.render_shader(COMP_SHADER, self.get_render_target('Comp'),
            textures= {
                'color_tex': inputs['Color'], 
                'dr_tex': self.get_output('DR_4', 'MAIN')
            },
            uniforms= {
                'auto_exposure': inputs['Auto Exposure'],
            }
        )

        outputs['Color'] = self.get_output('Comp', 'MAIN')

NODE = ToneMapper