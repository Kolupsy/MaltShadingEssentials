#ifndef SHADINGESSENTIALS_SHADERS_GLSL
#define SHADINGESSENTIALS_SHADERS_GLSL

#include "Input.internal.glsl"

/* META
    @base_color: default = (0.8, 0.8, 0.8, 1.0 );
    @normal : subtype = Normal; default = NORMAL;
    @light_group : default = 1;
    @shadows : default = true;
    @self_shadows : default = true;
*/
vec4 diffuse_shader( vec4 base_color, vec3 normal, int light_group, bool shadows, bool self_shadows ){
    vec4 result = base_color * vec4( diffuse_shading( POSITION, normal, light_group, shadows, self_shadows ), 1.0 );
    return result;
}

/* META
    @base_color: default = (0.8, 0.8, 0.8, 1.0 );
    @roughness : default = 0.3;
    @normal : subtype = Normal; default = NORMAL;
    @light_group : default = 1;
    @shadows : default = true;
    @self_shadows : default = true;
*/
vec4 specular_shader( vec4 base_color, float roughness, vec3 normal, int light_group, bool shadows, bool self_shadows ){
    return base_color * vec4( specular_shading( POSITION, normal, roughness, light_group, shadows, self_shadows ), 1.0 );
}

/*  META
    @base_color: default = ( 0.8, 0.8, 0.8, 1.0 );
    @roughness: default = 0.8;
    @normal: subtype=Normal; default=NORMAL;
*/
vec4 basic_pbr( vec4 base_color, float roughness, float metallic, vec3 normal ){

    vec4 diffuse_gradient = vec4( diffuse_shading( POSITION, normal, 1, true, true ), 1.0 );
    vec4 diffuse_color = base_color * diffuse_gradient;

    vec3 blended_normal = mix( normal, NORMAL, 0.5 );
    float facing, fresnel;
    layer_weight( 0.24, blended_normal, fresnel, facing );
    fresnel *= rgb_to_hsv( diffuse_color.rgb ).z;

    vec4 specular_gradient = vec4( specular_shading( POSITION, normal, roughness, 1, true, true ), 1.0 );
    specular_gradient.rgb = vec3_pow( specular_gradient.rgb, vec3( 1.5 ));
    specular_gradient.rgb *= vec3( 2 * ( 1.2 - roughness ));
    specular_gradient.rgb += vec3( fresnel * 0.5 );

    vec4 glossy_color = base_color * specular_gradient;
    vec4 dielectric_color = mix( specular_gradient, diffuse_color, roughness );
    vec4 result = mix( dielectric_color, glossy_color, metallic );
    return result;
}
/* META
    @color: default = (0.8, 0.8, 0.8, 1.0 );
    @brightness: default = 1.0;
    @mask: default = 1.0;
*/
vec4 emission( vec4 color, float brightness, float mask ){
    vec4 result = color;
    result.xyz *= vec3( brightness );
    result.a *= mask;
    return result;
}

#endif
