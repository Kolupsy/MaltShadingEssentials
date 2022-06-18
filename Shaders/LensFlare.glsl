
#include "Common.glsl"
#include "Filters/Blur.glsl"
#include "Node Utils/common.glsl"
#include "Common/Matrix.glsl"
#include "../ShaderFunctions/noise_functions.glsl"

vec2 aspect_ratio( ){
    vec2 res = render_resolution( );
    return vec2( res.x / res.y, 1.0 );
}

vec3 blend_in( vec3 color, float mask ){
    return clamp( color * vec3( mask ), 0.0, 1.0 );
}

vec3 sun_location( vec3 rotation ){
    mat4 rot_mat = mat4_rotation_from_euler( rotation );
    vec3 pos = transform_point( rot_mat, vec3( 0.0, 0.0, 99999 ));
    return pos + transform_point( CAMERA, vec3( 0.0 ));
}

vec3 world_to_camera( vec3 pos ){
    return transform_point( CAMERA, pos );
}

bool valid_camera_pos( vec3 pos ){
    return pos.z < 0.0;
}

vec2 camera_to_screen( vec3 pos ){
    vec2 pos_2D = vec2( pos.x / pos.z, pos.y / pos.z );
    return vec2( 0.5 ) - pos_2D;
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

float flare_occlusion( sampler2D depth_tex, vec2 uv, float dist = 99999 ){
    float d = texture( depth_tex, uv ).x;
    float a = box_blur( depth_tex, uv, 10.0, false ).a;
    if( a >= 0.5 ){
        a = min( a, ( d < dist )? 1.0 : 0.0 );
    }
    return a;
}

float radial_gradient( vec2 uv ){
    return ( atan( uv.y, uv.x ) + PI ) / ( PI * 2 );
}

float main_flare( vec2 uv, vec2 pos, float speed = 0.01, float diameter = 1.03, float bloom_size = 0.02, float streak_scale = 28.0, float intensity = 1.0 ){
    uv = uv - pos;
    uv *= aspect_ratio( );
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
    falloff *= 5.0;

    float bloom = pow(( diameter - dist ), 1.0 / bloom_size ) * intensity;

    streaks *= falloff;
    streaks += bloom;
    return ( streaks <= 0.0 ) ? 0.0 : streaks;
}

float flare_disk( vec2 uv, vec2 pos, float size, float intensity ){
    uv -= pos;
    uv *= aspect_ratio( );
    uv /= size;
    return ( 1.0 - pow( length( uv ), 1.5 )) * intensity;
}

float flare_circle( vec2 uv, vec2 pos, float size, float intensity, float focus = 10.0 ){
    
    uv -= pos;
    uv *= aspect_ratio( );
    uv /= size;
    float grad = abs( length( uv ) - 1.0 );
    float main_ring = grad * focus * PI;
    main_ring = cos( main_ring ) + 1.0;
    main_ring *= (( grad - ( 1.0 / focus )) < 0.0 )? 1.0 : 0.0;
    main_ring *= intensity;
    return main_ring;
}

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

layout (location = 0) out vec4 RESULT;

uniform sampler2D color_texture;
uniform sampler2D depth_texture;
uniform vec3 euler_rot;

void main()
{
    PIXEL_SETUP_INPUT();
    vec2 uv = UV[0];
    vec4 background = texture( color_texture, uv );
    RESULT = background;

    vec3 sun_world_pos = sun_location( euler_rot );
    vec3 sun_cam_pos = world_to_camera( sun_world_pos );
    if( !valid_camera_pos( sun_cam_pos )){
        return;
    }
    vec2 sun_2D = camera_to_screen( sun_cam_pos );
    float fo = flare_occlusion( depth_texture, sun_2D );
    if( fo >= 0.99 ){
        return;
    }
    float m = 1.0 - fo;
    vec3 flare_color = vec3( 1.0, 0.6, 0.4 );

    RESULT.xyz += blend_in( flare_color,
        main_flare( uv, flare_location( sun_2D, 1 ), 0.01, 1.03, 0.02, 19.0, m  )
    );

    RESULT.xyz += blend_in( flare_color,
        flare_circle( uv, flare_location( sun_2D, -0.6 ), 0.3, 0.005 * m, 7.0 )
    );

    RESULT.xyz += blend_in( flare_color, 
        flare_disk( uv, flare_location(sun_2D, -0.2 ), 0.07, 0.04 * m )
    );

    RESULT.xyz += blend_in( flare_color, 
        flare_disk( uv, flare_location( sun_2D, 0.6 ), 0.05, 0.04 * m )
    );

    RESULT.xyz += blend_in( flare_color,
        flare_disk( uv, flare_location( sun_2D, 0.1 ), 0.01, 0.02 * m )
    );
}

#endif
