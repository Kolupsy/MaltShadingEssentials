#ifndef SHADINGESSENTIALS_VECTOR_GLSL
#define SHADINGESSENTIALS_VECTOR_GLSL

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
    return vec3_divide( result, scale );
}
vec3 vector_mapping_vector( vec3 vector, vec3 rotation, vec3 scale ){
    return rotate_euler( vector * scale, rotation );
}
vec3 vector_mapping_normal( vec3 vector, vec3 rotation, vec3 scale ){
    return normalize( vector_mapping_vector( vector, rotation, scale ));
}

#endif