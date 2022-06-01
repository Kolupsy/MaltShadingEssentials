#ifndef SHADINGESSENTIALS_INPUT_GLSL
#define SHADINGESSENTIALS_INPUT_GLSL

#include "noise_functions.glsl"

vec3 incoming_vector( ){
    return normalize( POSITION - camera_position( ));
}

float fresnel_dielectric_cos( float cosi, float eta ){
    
    float c = abs( cosi );
    float g = eta * eta - 1.0 + c * c;
    float result;

    if( g > 0.0 ){
        g = sqrt(g);
        float A = (g - c) / (g + c);
        float B = (c * (g + c) - 1.0) / (c * (g - c) + 1.0);
        result = 0.5 * A * A * (1.0 + B * B);
    }
    else{
        result = 1.0;
    }
    return result;
}
float fresnel_dielectric( vec3 incoming, vec3 normal, float eta ){
    return fresnel_dielectric_cos( dot( incoming, normal ), eta );
}

vec3 object_coords( ){
    return transform_point( inverse( MODEL ), POSITION );
}
vec3 camera_mapping( ){
    return transform_point( CAMERA, POSITION ) * vec3( 1, 1, -1 );
}

void texture_coordinates( int uv_index, out vec3 generated, out vec3 normal, out vec2 uv, out vec3 object, out vec3 camera, out vec2 window, out vec3 reflection ){
    
    
    normal = transform_normal( inverse( MODEL ), NORMAL );
    uv = surface_uv( uv_index );
    object = object_coords( );
    generated = ( object + vec3( 1.0 )) * vec3( 0.5 );
    camera = camera_mapping( );
    window = screen_uv( );
    vec3 incoming = incoming_vector( );
    reflection = reflect( incoming, normalize( NORMAL ));
}

void geometry_info(
    out vec3 position, 
    out vec3 normal, 
    out vec3 tangent, 
    out vec3 _true_normal, 
    out vec3 incoming, 
    out vec2 parametric, 
    out float backfacing, 
    out float _curvature,
    out float random_island ){

        position = POSITION;
        normal = NORMAL;
        tangent = radial_tangent( NORMAL, vec3( 0, 0, 1 ));
        _true_normal = true_normal( );
        incoming = incoming_vector( );
        parametric = vec2( 0.0 );
        backfacing = 1.0 - float(is_front_facing( ));
        _curvature = curvature( );
        random_island = float( 0.0 );
    }

void camera_data( out vec3 view, out float depth, out float dist ){
    depth = abs( transform_point( CAMERA, POSITION ).z );
    vec3 cam_pos = camera_position( );
    dist = distance( POSITION, cam_pos );
    view = camera_mapping( );
}

void screenspace_info( out vec2 flat_uv, out vec2 projected, out vec2 matcap, out vec2 screen ){
    vec3 camera = camera_mapping( );
    flat_uv = vec2( camera.x / camera.z, camera.y / camera.z );
    projected = camera.xy;
    matcap = matcap_uv( NORMAL );
    screen = screen_uv( );
}

void layer_weight(float blend, vec3 normal, out float fresnel, out float facing)
{
  normal = normalize( normal );

  /* fresnel */
  float eta = max(1.0 - blend, 0.00001);
  vec3 V = incoming_vector( );

  fresnel = fresnel_dielectric(V, normal, (is_front_facing( )) ? 1.0 / eta : eta);

  /* facing */
  facing = abs(dot(V, normal));
  if (blend != 0.5) {
    blend = clamp(blend, 0.0, 0.99999);
    blend = (blend < 0.5) ? 2.0 * blend : 0.5 / (1.0 - blend);
    facing = pow(facing, blend);
  }
  facing = 1.0 - facing;
}

/*  META
    @base_color: default = 0.3;
*/
float line_world_scale( float scale ){
    return float_divide( 1, float_pow( pixel_world_size( ), 0.5 )) * scale;
}

/* META
    @global_width: default = 0.3;
    @depth_influence: default = 0.8;
    @normal_influence: default = 0.5;
*/
float tapered_lines( float global_width, float depth_influence, float normal_influence ){
    return line_width( line_world_scale( global_width ), vec4( 1 ), depth_influence, -0.2, 0.1, 1, normal_influence, -0.2, 0.6, 1 );
}

/* META
    @global_width: default =  0.8;
    @depth_influence: default = 0.8;
    @normal_influence: default = 0.5;
    @noise_scale: default = 2.5;
    @bias: default = 0.7;
*/
float noisy_lines( float global_width, float depth_influence, float normal_influence, float noise_scale, float bias ){

    float width = tapered_lines( global_width, depth_influence, normal_influence );
    float noise = clamp( fractal_noise3D( POSITION * vec3( noise_scale ), 2, 0.5 ) - ( 1 - bias ), 0, 1 );
    return width * noise;
}

vec3 tangent_uv_tangent( vec2 uv ){
    return compute_tangent( uv ).xyz;
}
vec3 tangent_radial( vec3 vector ){
    return vec3( 0.0 );
}

#endif