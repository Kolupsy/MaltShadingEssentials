#ifndef SHADINGESSENTIALS_INPUT_GLSL
#define SHADINGESSENTIALS_INPUT_GLSL

#include "noise_functions.internal.glsl"
#include "Vector.internal.glsl"
#include "Utils.internal.glsl"

#include "Common/Transform.glsl"
#include "Common/Normal.glsl"

#include "Node Utils/common.glsl"
#include "Node Utils/packing.glsl"

#include "NPR_Pipeline/NPR_Filters.glsl"

vec3 incoming_vector( ){
    return normalize( camera_position( ) - POSITION );
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
    vec3 incoming = normalize( incoming_vector( ) * vec3( -1.0 ));
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
        #ifdef NPR_FILTERS_ACTIVE
        _curvature = curvature( );
        #else
        _curvature = 0.0;
        #endif
        random_island = float( 0.0 );
    }

void object_info( out vec3 location, out vec3 scale, out mat4 matrix, out float dist, out vec4 id, out vec4 random ){

    location = model_position( );
    matrix = model_matrix( );
    scale = vec3( length(matrix[0].xyz), length(matrix[1].xyz), length(matrix[2].xyz));
    dist = distance( location, transform_point( inverse( camera_matrix( )), vec3( 0 )));
    vec4 crap_1;
    vec4 crap_2;
    vec4 crap_3;
    unpack_8bit( object_original_id( ), id, crap_1, crap_2, crap_3 );
    random = hash_vec4_to_vec4( id );
}

void camera_data( out vec3 view, out float depth, out float dist ){
    depth = abs( transform_point( CAMERA, POSITION ).z );
    vec3 cam_pos = camera_position( );
    dist = distance( POSITION, cam_pos );
    view = camera_mapping( );
}

void screenspace_info( out vec2 flat_uv, out vec2 projected, out vec2 matcap, out vec2 screen, bool is_screen_shader ){
    vec3 camera = camera_mapping( );
    if( is_screen_shader ){
        vec2 res = render_resolution( );
        float aspect = res.x / res.y;
        flat_uv = ( screen_uv( ) - vec2( 0.5 )) * vec2( aspect, 1.0 );
    }else{
        flat_uv = vec2( camera.x / camera.z, camera.y / camera.z );
    }
    projected = camera.xy;
    matcap = matcap_uv( NORMAL );
    screen = screen_uv( );
}

void layer_weight(float blend, vec3 normal, out float fresnel, out float facing)
{
  normal = normalize( normal );

  /* fresnel */
  float eta = max(1.0 - blend, 0.00001);
  vec3 V = normalize( incoming_vector( ));

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

float line_world_scale( float scale ){
    return ( 1 / pow( pixel_world_size( ), 0.5 )) * scale;
    // return float_divide( 1, float_pow( pixel_world_size( ), 0.5 )) * scale;
}

/* META
    @global_width: default = 0.3;
    @depth_influence: default = 0.8;
    @normal_influence: default = 0.5;
*/
float tapered_lines( float global_width, float depth_influence, float normal_influence, vec4 id_bounds ){
    return line_width( line_world_scale( global_width ), id_bounds, depth_influence, -0.2, 0.1, 1, normal_influence, -0.2, 0.6, 1 );
}

/* META
    @global_width: default =  0.8;
    @depth_influence: default = 0.8;
    @normal_influence: default = 0.5;
    @noise_scale: default = 2.5;
    @bias: default = 0.7;
*/
float noisy_lines( float global_width, float depth_influence, float normal_influence, vec4 id_bounds, float noise_scale, float bias ){

    float width = tapered_lines( global_width, depth_influence, normal_influence, id_bounds );
    float noise = clamp( fractal_noise3D( POSITION * vec3( noise_scale ), 2, 0.5 ) - ( 1 - bias ), 0, 1 );
    return width * noise;
}

vec3 tangent_uv_tangent( vec2 uv ){
    return compute_tangent( uv ).xyz;
}

/* META
    @offset: subtype = Vector;
    @rotation: subtype = Vector;
*/
vec3 tangent_radial( vec3 offset, vec3 rotation ){
    vec3 co = object_coords( );
    co = rotate_euler( co + offset, rotation );
    co = vec3( - co.y, co.x, 0.0 );
    co = transform_point( MODEL, co );
    co = normalize( cross( co, NORMAL ));
    return cross( NORMAL, co );
}

/* META
    @world_coordinates: default = view_direction( );
*/
vec3 sky_coords( vec3 world_coordinates, float horizon = 0.0 ){
    float z = world_coordinates.z + horizon;
    return vec3( world_coordinates.x / z, world_coordinates.y / z, pow( z, 0.5 ));
}

/* META
    @position: default = POSITION;
    @tangent: default = compute_tangent( UV[0] ).xyz;
    @normal: default = NORMAL;
*/
vec3 parallax_mapping( vec3 position, vec3 tangent, vec3 normal, float depth ){
    vec3 incoming = incoming_vector( ) * vec3( -1.0 );
    vec3 offset_position = position - incoming * vec3( depth );
    vec3 bitangent = cross( normal, tangent );
    return vec3(
        dot( offset_position, tangent ),
        dot( bitangent, offset_position ),
        dot( offset_position, normal )
    );
}

/* META
    @position: default = POSITION;
    @incoming: default = incoming_vector( );
    @room_dimensions: default = vec3( 1.0 );
*/
void interior_mapping( vec3 position, vec3 incoming, vec3 room_dimensions, out vec3 mapping, out vec4 wall_masks, out float wall_index ){
    vec3 incoming_T = transform_direction( inverse( MODEL ), incoming ) * vec3( -1.0 );
    vec3 position_T = transform_point( inverse( MODEL ), position );
    float coord_z = room_dimensions.z * (( incoming_T.z > 0.0 )? 1.0 : -1.0 );
    wall_masks.x = clamp( coord_z, 0.0, 1.0 );
    wall_masks.x = coord_z > 0.0? 1.0 : 0.0;
    vec3 walls_z = ray_hit( incoming_T, position_T, position_T.z, incoming_T.z, coord_z );
    vec3 walls_z_T = walls_z + vec3( 1.0, 0.0, 0.0 );
    float wall_z_l = length( walls_z );

    float coord_x = room_dimensions.x * (( incoming_T.x > 0.0 )? 1.0 : -1.0 );
    wall_masks.y = clamp( coord_x, 0.0, 1.0 );
    wall_masks.y = coord_x > 0.0? 1.0 : 0.0;
    vec3 walls_x = ray_hit( incoming_T, position_T, position_T.x, incoming_T.x, coord_x );
    vec3 walls_x_T = vector_mapping_texture( walls_x, vec3( 0.0, 0.0, 1.0 ), vec3( 0.0, PI * 0.5, 0.0 ), vec3( 1.0, 1.0, 1.0 )).yxz;
    walls_x_T.y = 2.0 - walls_x_T.y;
    float wall_x_l = length( walls_x );

    vec3 walls_y = ray_hit( incoming_T, position_T, position_T.y, incoming_T.y, room_dimensions.y * 2.0 );
    vec3 walls_y_T = vector_mapping_texture( walls_y, vec3( -1.0, 0.0, -1.0 ), vec3( PI * 0.5, 0.0, 0.0 ), vec3( 1.0 ));
    float wall_y_l = length( walls_y );

    wall_masks.z = ( wall_z_l < wall_x_l )? 1.0 : 0.0;
    vec3 result = mix( walls_x_T, walls_z_T, wall_masks.z );
    wall_masks.w = ( min( wall_z_l, wall_x_l ) < wall_y_l )? 0.0 : 1.0;
    result = ( min( wall_z_l, wall_x_l ) < wall_y_l )? result : walls_y_T;
    mapping = result * vec3( 0.5 );

    float wall_1_mask = wall_masks.z * ( 1.0 - wall_masks.w ) * wall_masks.x;
    float wall_2_mask = wall_masks.y * ( 1.0 - wall_masks.z ) * ( 1.0 - wall_masks.w );
    float wall_3_mask = ( 1.0 - wall_masks.z ) * ( 1.0 - wall_masks.w ) * ( 1.0 - wall_masks.y );
    float wall_4_mask = wall_masks.w;
    wall_index = mix( 0.0, 1.0, wall_1_mask );
    wall_index = mix( wall_index, 2.0, wall_2_mask );
    wall_index = mix( wall_index, 3.0, wall_3_mask );
    wall_index = mix( wall_index, 4.0, wall_4_mask );    
}

#endif
