
#include "Common.glsl"
#include "Filters/Blur.glsl"
#include "Node Utils/common.glsl"
#include "Common/Matrix.glsl"
#include "../ShaderFunctions/noise_functions.glsl"

vec2 aspect_ratio( ){
    vec2 res = render_resolution( );
    return vec2( res.x / res.y, 1.0 );
}

vec2 screenspace( vec2 uv ){
    uv -= vec2( 0.5 );
    return uv * aspect_ratio( );
}

vec2 sun_pos_on_screen( vec3 rotation ){
    mat4 rot_mat = mat4_rotation_from_euler( rotation );
    vec3 pos = transform_point( rot_mat, vec3( 0.0, 0.0, 99999 ));
    pos += transform_point( CAMERA, vec3( 0.0 ));
    pos = transform_point( CAMERA, pos );
    pos = transform_point( projection_matrix( ), pos );
    vec2 pos_2D = vec2( pos.x / pos.z, pos.y / pos.z );
    return pos_2D;
}

float sigmoid( float gradient, float a, float b ){
    float e = 2.71828;
    return 1.0 / ( 1 + pow( e, - a * ( gradient - b )));
}

float radial_gradient( vec2 uv ){
    return ( atan( uv.y, uv.x ) + PI ) / ( PI * 2 );
}

float ngon_shape( vec2 uv, int sides ){

    float ratio = 1.0 / float( sides );
    vec2 grad_uv = rotate_2d( uv, PI / float( sides ));
    float angle = radial_gradient( grad_uv );
    angle = floor(( angle / ratio )) * ratio;
    angle = angle * ( -PI * 2 );
    uv = rotate_2d( uv, angle );
    return - uv.x;
}

float ring( vec2 uv, float radius, float thickness ){
    float grad = abs( length( uv ) - radius );
    grad = 1 - grad * ( 1 / thickness );
    return grad;
}

float main_flare( vec2 uv, vec2 pos, float speed = 0.01, float diameter = 1.03, float bloom_size = 0.02, float streak_scale = 28.0 ){
    uv = uv + pos;
    float time = current_time( ) * speed;
    float grad1 = abs( radial_gradient( rotate_2d( uv, time * 1.3 + pos.x * 0.5 )) - 0.5);
    float grad2 = abs( radial_gradient( rotate_2d( uv, 4.4 - time / 0.4 + pos.x * 0.5 )) - 0.5 );
    float streaks1 = fractal_noise1D( grad1 * streak_scale, 1.0, 0.2 );
    float streaks2 = fractal_noise1D( grad2 * streak_scale, 1.0, 0.2 );
    float streaks = pow( mix( streaks1, streaks2, 0.5 ) - 0.21, 1.28 );
    streaks = clamp( streaks, 0.0, 1.0 );

    float dist = length( uv );
    float falloff = pow( dist, 0.011 );
    falloff = clamp( 1.0 - falloff, 0.0, 1.0 );
    falloff *= 5.0;

    float bloom = pow(( diameter - dist ), 1.0 / bloom_size );

    streaks *= falloff;
    streaks += bloom;

    return streaks;
}

float flare_disk( vec2 uv, vec2 pos, float size, float intensity ){
    uv = uv + pos;
    uv /= size;
    return ( 1.0 - pow( length( uv ), 1.5 )) * intensity;
}

float flare_circle( vec2 uv, vec2 pos, float size, float intensity ){
    float thickness = 10.0;
    
    uv += pos;
    uv /= size;
    float grad = abs( length( uv ) - 1.0 );
    float main_ring = grad * thickness * PI;
    main_ring = cos( main_ring ) + 1.0;
    main_ring *= (( grad - ( 1.0 / thickness )) < 0.0 )? 1.0 : 0.0;
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
    vec2 ss = screenspace( uv );
    vec2 sun_pos = sun_pos_on_screen( euler_rot );
    float d = length(( uv - sun_pos - vec2( 0.5 )) * aspect_ratio( ));

    RESULT = vec4( vec3( d ), 1.0 );
}

#endif
