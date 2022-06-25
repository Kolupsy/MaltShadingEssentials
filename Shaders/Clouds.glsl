
#include "Common.glsl"
#include "Common/Transform.glsl"

#include "Node Utils/common.glsl"

#include "../ShaderFunctions/Utils.internal.glsl"
#include "../ShaderFunctions/Input.internal.glsl"
#include "../ShaderFunctions/Vector.internal.glsl"
#include "../ShaderFunctions/noise_functions.internal.glsl"
#include "../ShaderFunctions/Textures.internal.glsl"

float smoother_step( float value, float from_min, float from_max, float to_min, float to_max ){

    if ( from_max != from_min ) {
        float x;
        float factor;
        if( from_min > from_max ) {
            x = clamp(( value - from_max ) / ( from_min - from_max ), 0.0, 1.0);
            x = (x * x * x * (x * (x * 6.0 - 15.0) + 10.0));
            factor = 1.0 - x;
        } else {
            x = clamp(( value - from_min ) / ( from_max - from_min ), 0.0, 1.0);
            x = (x * x * x * (x * (x * 6.0 - 15.0) + 10.0));
            factor = x;
        }
        return to_min + factor * ( to_max - to_min );
    }
    else {
        return 0.0;
    }
}

vec2 distortion_noise( vec2 uv, float scale, float detail, float roughness ){
    vec2 p = uv * scale;
    return vec2(
        fractal_noise2D( p + random_vec2_offset( 1.0 ), detail, roughness ),
        fractal_noise2D( p + random_vec2_offset( 2.0 ), detail, roughness ));
}

float cloud_voronoi( vec2 coord,
                    float scale){
  float randomness = 1.0;

  vec2 scaledCoord = coord.xy * scale;
  vec2 cellPosition = floor(scaledCoord);
  vec2 localPosition = scaledCoord - cellPosition;

  float minDistance = 8.0;
  for (int j = -1; j <= 1; j++) {
    for (int i = -1; i <= 1; i++) {
      vec2 cellOffset = vec2(i, j);
      vec2 pointPosition = cellOffset + hash_vec2_to_vec2(cellPosition + cellOffset) * randomness;
      float distanceToPoint = voronoi_distance2D(pointPosition, localPosition, 0, 2.0 );
      if (distanceToPoint < minDistance) {
        minDistance = distanceToPoint;
      }
    }
  }
  return minDistance;
}

float main_cloud_layer( vec2 uv, float v_scale, float n_scale, float n_detail, float n_roughness, float distortion ){
    vec2 d = distortion_noise( uv, n_scale, n_detail, n_roughness );
    uv = vector_distortion( uv, d, distortion );
    return cloud_voronoi( uv, v_scale );
}

float streak_cloud_layer( vec2 uv, float v_scale, float n_scale, float n_detail, float n_roughness, vec2 aspect, float distortion ){
    vec2 d = distortion_noise( uv, n_scale, n_detail, n_roughness );
    uv = vector_distortion( uv, d, distortion );
    uv *= aspect;
    return cloud_voronoi( uv, v_scale );
}

#ifdef VERTEX_SHADER
void main()
{
    DEFAULT_SCREEN_VERTEX_SHADER();
}
#endif

#ifdef PIXEL_SHADER

uniform float main_cloud_strength; //0.6
uniform float streak_cloud_strength; //0.3
uniform float wind_speed; //0.05
uniform float wind_angle;

layout (location = 0) out vec4 RESULT;

void main()
{
    PIXEL_SETUP_INPUT( );
    RESULT = vec4( 1.0 );
    vec3 world_coords = view_direction( );
    vec3 coords = sky_coords( world_coords, 0.033 );
    float time = current_time( );

    float clouds;
    if( main_cloud_strength > 0.0 ){
        vec2 big_offset = rotate_2d( vec2( time * wind_speed * 0.5, 0.0 ), wind_angle );
        float big = main_cloud_layer( coords.xy + big_offset, 0.28, 0.28, 1.0, 0.7, 2.0 );
        vec2 medium_offset = rotate_2d( vec2( time * wind_speed, 0.0 ), wind_angle ) + big_offset;
        float medium = main_cloud_layer( coords.xy + medium_offset, 1.54, 0.64, 2.8, 0.7, 1.58 );
        float small = main_cloud_layer( coords.xy + medium_offset, 7.473, 5.69, 2.0, 0.7, 0.284 );
        
        clouds = mix( big, medium, 0.297 );
        clouds = mix( clouds, small, 0.072 );
        float size_gradient = smoother_step( coords.z, 0.0, 1.0, 0.3, 0.6 );
        clouds = smoother_step( clouds, 0.12, size_gradient, 1.0, 0.0 );
        clouds = ( world_coords.z > 0.0 )? clouds : 0.0;
        clouds *= main_cloud_strength;
    }
    
    float streaks;
    if( streak_cloud_strength > 0.0 ){
        vec2 streaks_offset = vec2( 0.0, time * 0.03 );
        streaks = streak_cloud_layer( coords.xy + streaks_offset, 0.9, 0.46, 2.0, 0.3, vec2( 0.1, 1.0 ), 1.0 );
        streaks = smoother_step( streaks, 0.0, 0.33, 1.0, 0.0 );
        streaks *= coords.z;
        streaks *= streak_cloud_strength;
    }    

    clouds = max( clouds, streaks );
    RESULT.xyz = vec3( clouds );
}

#endif