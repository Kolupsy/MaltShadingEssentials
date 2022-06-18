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

float sigmoid( float gradient, float a, float b ){
    float e = 2.71828;
    return 1.0 / ( 1 + pow( e, - a * ( gradient - b )));
}

vec2 screenspace( vec2 uv ){
    uv -= vec2( 0.5 );
    return uv * aspect_ratio( );
}