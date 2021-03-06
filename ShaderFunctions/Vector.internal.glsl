#ifndef SHADINGESSENTIALS_VECTOR_GLSL
#define SHADINGESSENTIALS_VECTOR_GLSL

#include "Common/Transform.glsl"
#include "Common/Matrix.glsl"
#include "Common/Quaternion.glsl"

mat4 rotation_matrix_axis_angle( vec3 axis, float angle ){
    return mat4_rotation_from_quaternion( quaternion_from_axis_angle( normalize( axis ), angle ));
}

vec3 rotate_axis_angle( vec3 vector, vec3 axis, float angle ){
    return transform_direction( rotation_matrix_axis_angle( axis, angle ), vector );
}
vec3 rotate_axis_angle_inverted( vec3 vector, vec3 axis, float angle ){
    return transform_direction( inverse( rotation_matrix_axis_angle( axis, angle )), vector );
}

vec3 rotate_euler( vec3 vector, vec3 euler ){
    return transform_direction( mat4_rotation_from_euler( euler ), vector );
}
vec3 rotate_euler_inverted( vec3 vector, vec3 euler ){
    return transform_direction( inverse( mat4_rotation_from_euler( euler )), vector );
}

float vector_angle( vec3 a, vec3 b ){

    return acos(dot( a, b ) / (length( a ) * length( b )));
}

vec3 vector_mapping_point( vec3 vector, vec3 location, vec3 rotation, vec3 scale ){
    vec3 result = vector * scale;
    result = rotate_euler( result, rotation );
    return result + location;
}
vec3 vector_mapping_texture( vec3 vector, vec3 location, vec3 rotation, vec3 scale ){
    vec3 result = vector - location;
    result = rotate_euler_inverted( result, rotation );
    return result / scale;
}
vec3 vector_mapping_vector( vec3 vector, vec3 rotation, vec3 scale ){
    return rotate_euler( vector * scale, rotation );
}
vec3 vector_mapping_normal( vec3 vector, vec3 rotation, vec3 scale ){
    return normalize( vector_mapping_vector( vector, rotation, scale ));
}

float vector_angle_2D( vec2 vector ){
    return atan( vector.y, vector.x );

}
float vector_angle_2D_continuous( vec2 vector ){
    float tang = vector_angle_2D( vector );
    return ( tang < 0.0 )
            ? PI * 2.0 + tang 
            : tang;
}

vec2 object_view_orientation( vec3 vector, vec3 location, vec3 rotation, vec3 scale ){
    vec3 point_A = location;
    vec3 point_B = vector_mapping_point( vector, location, rotation, scale );
    point_A = transform_point( CAMERA, point_A );
    point_B = transform_point( CAMERA, point_B );
    vec2 point_A_2D = vec2( point_A.x / point_A.z, point_A.y / point_A.z );
    vec2 point_B_2D = vec2( point_B.x / point_B.z, point_B.y / point_B.z );
    return point_A_2D - point_B_2D;
}

vec2 vector_distortion( vec2 vector, vec2 distortion, float factor ){
    distortion -= vec2( 0.5 );
    distortion *= vec2( factor );
    return vector + distortion;
}

vec3 vector_distortion( vec3 vector, vec3 distortion, float factor ){

    distortion -= vec3( 0.5 );
    distortion *= vec3( factor );
    return vector + distortion;
}

vec4 vector_distortion( vec4 vector, vec4 distortion, float factor ){

    distortion -= vec4( 0.5 );
    distortion *= vec4( factor );
    return vector + distortion;
}

#endif
