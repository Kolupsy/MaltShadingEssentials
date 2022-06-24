
#include "Common.glsl"
#include "Common/Matrix.glsl"
#include "Common/Color.glsl"

#include "Filters/Blur.glsl"
#include "Node Utils/common.glsl"

#include "Lighting/Lighting.glsl"

#include "../ShaderFunctions/noise_functions.internal.glsl"
#include "../ShaderFunctions/Utils.internal.glsl"

vec3 blend_in( vec3 color, float mask ){
    return clamp( color * vec3( mask ), 0.0, 1.0 );
}
vec3 blend_in( vec3 color, vec3 mask ){
    return clamp( color * mask, 0.0, 1.0 );
}

vec3 light_world_location( Light light ){
    if( !( light.type == 1 )){
        return light.position;
    }else{
        return vec3( - 9999.0 ) * light.direction + camera_position( );
    }
}

float light_intensity_coef( Light light, vec3 light_factors, float view_distance ){
    return clamp( 1.0 * length( light.color ), 0.0, 99.0 );
}

bool valid_camera_pos( vec3 pos ){
    return pos.z < 0.0;
}

vec2 camera_to_screen( vec3 pos ){
    pos = transform_point( projection_matrix( ), pos );
    vec2 pos_2D = vec2( pos.x / pos.z, pos.y / pos.z );
    pos_2D *= vec2( 0.5 );
    pos_2D += vec2( 0.5 );
    return pos_2D;
}

vec2 sun_pos_on_screen( vec3 rotation ){
    mat4 rot_mat = mat4_rotation_from_euler( rotation );
    vec3 pos = transform_point( rot_mat, vec3( 0.0, 0.0, 99999 ));
    pos += transform_point( CAMERA, vec3( 0.0 ));
    pos = transform_point( CAMERA, pos );
    vec2 pos_2D = vec2( pos.x / pos.z, pos.y / pos.z );
    return vec2( 0.5 ) - pos_2D;
}

vec2 flare_location( vec2 source_pos, float line_pos ){
    vec2 m = vec2( 0.5 );
    vec2 v = source_pos - m;
    return m + vec2( line_pos ) * v;
}
vec2 flare_uv( vec2 uv, vec2 source_pos, float line_pos ){
    vec2 fl = flare_location( source_pos, line_pos );
    uv -= fl;
    uv *= aspect_ratio( );
    return uv;
}

float flare_occlusion( sampler2D depth_tex, vec2 uv, float blur = 5.0 ){
    float a = box_blur( depth_tex, uv, blur, false ).a * 2.0;
    return a;
}

float radial_gradient( vec2 uv ){
    return ( atan( uv.y, uv.x ) + PI ) / ( PI * 2 );
}

float main_flare( vec2 uv, vec2 pos, float speed = 0.01, float diameter = 1.03, float bloom_size = 0.02, float streak_scale = 28.0, float intensity = 1.0 ){

    float time = current_time( ) * speed;
    float grad1 = abs( radial_gradient( rotate_2d( uv, time * 1.3 + pos.x * 0.5 )) - 0.5);
    float grad2 = abs( radial_gradient( rotate_2d( uv, 4.4 - time / 0.4 + pos.x * 0.5 )) - 0.5 );
    float streaks1 = fractal_noise1D( grad1 * streak_scale, 1.0, 0.2 );
    float streaks2 = fractal_noise1D( grad2 * streak_scale, 1.0, 0.2 );
    float streaks = pow( mix( streaks1, streaks2, 0.5 ) - 0.21, 1.28 );
    streaks = clamp( streaks * intensity, 0.0, 1.0 );

    float dist = length( uv );
    float falloff = pow( dist, 0.011 * intensity );
    falloff = clamp( 1.0 - falloff, 0.0, 1.0 );
    falloff *= 10.0;

    float bloom = pow(( diameter - dist ), 1.0 / bloom_size ) * ( intensity * 0.5 );

    streaks *= falloff;
    streaks += bloom;
    return ( streaks <= 0.0 ) ? 0.0 : streaks;
}

float flare_disk( vec2 uv, float size, float intensity ){
    uv /= size;
    return ( 1.0 - pow( length( uv ), 1.5 )) * intensity;
}
vec3 flare_disk_disp( vec2 uv, vec2 source_pos, float line_pos, float dispersion, float size, float intensity ){
    vec2 red_uv = flare_uv( uv, source_pos, line_pos * ( 1.0 - dispersion ));
    vec2 green_uv = flare_uv( uv, source_pos, line_pos );
    vec2 blue_uv = flare_uv( uv, source_pos, line_pos * ( 1.0 + dispersion ));
    return vec3(
        flare_disk( red_uv, size, intensity ),
        flare_disk( green_uv, size, intensity ),
        flare_disk( blue_uv, size, intensity )
    );
}

float flare_circle( vec2 uv, float size, float intensity, float focus = 10.0 ){

    uv /= size;
    float grad = abs( length( uv ) - 1.0 );
    float main_ring = grad * focus * PI;
    main_ring = cos( main_ring ) + 1.0;
    main_ring *= (( grad - ( 1.0 / focus )) < 0.0 )? 1.0 : 0.0;
    main_ring *= intensity;
    return main_ring;
}
vec3 flare_circle_disp( vec2 uv, vec2 source_pos, float line_pos, float dispersion, float size, float intensity, float focus = 10.0 ){
    vec2 red_uv = flare_uv( uv, source_pos, line_pos * ( 1.0 - dispersion ));
    vec2 green_uv = flare_uv( uv, source_pos, line_pos );
    vec2 blue_uv = flare_uv( uv, source_pos, line_pos * ( 1.0 + dispersion ));
    return vec3(
        flare_circle( red_uv, size, intensity, focus ),
        flare_circle( green_uv, size, intensity, focus ),
        flare_circle( blue_uv, size, intensity, focus )
    );
}

vec3 lens_flare_stack( vec2 uv, vec3 light_color, vec2 light_2D, float intensity ){
    vec3 result = vec3( 0.0 );

    result += blend_in( light_color,
        main_flare( flare_uv( uv, light_2D, 1.0 ), light_2D, 0.03, 1.03, 0.02, 19.0, intensity  )
    );
    result += blend_in( light_color,
        flare_circle_disp( uv, light_2D, -0.6, 0.05, 0.3, 0.015 * intensity, 7.0 )
    );
    result += blend_in( light_color, 
        flare_disk_disp( uv, light_2D, -0.2, 0.05, 0.1, 0.1 * intensity )
    );
    result += blend_in( light_color,
        flare_disk_disp( uv, light_2D, 0.6, 0.05, 0.06, 0.1 * intensity )
    );
    result += blend_in( light_color,
        flare_disk_disp( uv, light_2D, 0.1, 0.05, 0.02, 0.08 * intensity )
    );

    return result;
}


#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

layout( location = 0 ) out vec4 RESULT;

uniform sampler2D color_texture;
uniform sampler2D occlusion_texture;
uniform vec3 light_factors;
uniform float edge_fade;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];
    vec4 background = texture( color_texture, uv );
    RESULT = background;

    for( int i = 0; i < LIGHTS.lights_count; i++ ){
        Light light = LIGHTS.lights[ i ];
        if( light.type != 1 ){
            continue;
        }
        if( length( light.color ) == 0.0 ){
            continue;
        }
        vec3 lwl = light_world_location( light );
        vec3 cam_pos = transform_point( CAMERA, lwl );
        if( !valid_camera_pos( cam_pos )){
            continue;
        }
        vec2 light_2D = camera_to_screen( cam_pos );
        float view_distance = abs( length( light.position - camera_position( )));
        float lfo = flare_occlusion( occlusion_texture, light_2D, edge_fade );
        if( lfo >= 0.99 ){
            continue;
        }
        vec3 mix_color = mix( light.color, light.color * texture( color_texture, light_2D ).xyz, lfo );
        RESULT.xyz += lens_flare_stack( uv, mix_color, light_2D, ( 1.0 - lfo ) * light_intensity_coef( light, light_factors, view_distance ));
    }
}

#endif
