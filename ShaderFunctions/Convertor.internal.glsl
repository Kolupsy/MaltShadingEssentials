#ifndef SHADINGESSENTIALS_CONVERTOR_GLSL
#define SHADINGESSENTIALS_CONVERTOR_GLSL

void float_map_range_linear( float value, float from_min, float from_max, float to_min, float to_max, int steps, out float result ){
    if( from_max != from_min ){
        result = ( value - from_min ) * (( to_max - to_min )/( from_max - from_min )) + to_min;
    }
    else{
        result = 0.0;
    }
}
void float_map_range_stepped( float value, float from_min, float from_max, float to_min, float to_max, int steps, out float result ){
  if ( from_max != from_min ){
    float factor = ( value - from_min ) / ( from_max - from_min );
    factor = ( steps > 0.0 ) ? floor( factor * ( steps + 1.0 )) / steps : 0.0;
    result = to_min + factor * ( to_max - to_min );
  }
  else{
    result = 0.0;
  }
}
void float_map_range_smoothstep( float value, float from_min, float from_max, float to_min, float to_max, int steps, out float result ){
    if ( from_max != from_min ) {
        float factor = ( from_min > from_max ) ? 1.0 - smoothstep( from_max, from_min, value ) : smoothstep(from_min, from_max, value );
        result = to_min + factor * ( to_max - to_min );
    }
    else {
        result = 0.0;
    }
}

void float_map_range_smootherstep( float value, float from_min, float from_max, float to_min, float to_max, int steps, out float result ){
    if ( from_max != from_min ) {
        float x;
        float factor;
        if( from_min > from_max ) {
            x = clamp(float_divide(( value - from_max ), ( from_min - from_max )), 0.0, 1.0);
            x = (x * x * x * (x * (x * 6.0 - 15.0) + 10.0));
            factor = 1.0 - x;
        } else {
            x = clamp(float_divide(( value - from_min ), ( from_max - from_min )), 0.0, 1.0);
            x = (x * x * x * (x * (x * 6.0 - 15.0) + 10.0));
            factor = x;
        }
        result = to_min + factor * ( to_max - to_min );
    }
    else {
        result = 0.0;
    }
}

#endif