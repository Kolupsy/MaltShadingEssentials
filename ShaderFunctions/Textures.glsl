#ifndef SHADINGESSENTIALS_TEXTURES_GLSL
#define SHADINGESSENTIALS_TEXTURES_GLSL

#include "noise_functions.glsl"
#include "Input.glsl"
#include "Math.glsl"

// PERLIN NOISE =================================================================================

void noise_texture1D( float w, float scale, float detail, float roughness, out float value, out vec4 color ){

    float p = w * scale;
    value = fractal_noise1D( p, detail, roughness );
    color = vec4( 
        value,
        fractal_noise1D( p + random_float_offset( 1.0 ), detail, roughness ),
        fractal_noise1D( p + random_float_offset( 2.0 ), detail, roughness ),
        fractal_noise1D( p + random_float_offset( 3.0 ), detail, roughness ));
}

void noise_texture2D( vec2 uv, float scale, float detail, float roughness, out float value, out vec4 color ){
    
    vec2 p = uv * scale;
    value = fractal_noise2D( p, detail, roughness );
    color = vec4(
        value,
        fractal_noise2D( p + random_vec2_offset( 2.0 ), detail, roughness ),
        fractal_noise2D( p + random_vec2_offset( 3.0 ), detail, roughness ),
        fractal_noise2D( p + random_vec2_offset( 4.0 ), detail, roughness ));
}

void noise_texture3D( vec3 vector, float scale, float detail, float roughness, out float value, out vec4 color ){

    vec3 p = vector * scale;
    value = fractal_noise3D( p, detail, roughness );
    color = vec4(
        value,
        fractal_noise3D( p + random_vec3_offset( 3.0 ), detail, roughness ),
        fractal_noise3D( p + random_vec3_offset( 4.0 ), detail, roughness ),
        fractal_noise3D( p + random_vec3_offset( 5.0 ), detail, roughness ));
}

void noise_texture4D( vec4 vector, float scale, float detail, float roughness, out float value, out vec4 color ){

    vec4 p = vector * scale;
    value = fractal_noise4D( p, detail, roughness );
    color = vec4(
        value,
        fractal_noise4D( p + random_vec4_offset( 4.0 ), detail, roughness ),
        fractal_noise4D( p + random_vec4_offset( 5.0 ), detail, roughness ),
        fractal_noise4D( p + random_vec4_offset( 6.0 ), detail, roughness ));
}

// CELL NOISE =================================================================================

void voronoi_texture_f1_1d( 
                            float w,
                            float scale,
                            float smoothness,
                            float exponent,
                            float randomness,
                            float metric,
                            out float outDistance,
                            out vec4 outColor,
                            out vec3 outPosition,
                            out float outW,
                            out float outRadius){

  randomness = clamp(randomness, 0.0, 1.0);

  float scaledCoord = w * scale;
  float cellPosition = floor(scaledCoord);
  float localPosition = scaledCoord - cellPosition;

  float minDistance = 8.0;
  float targetOffset, targetPosition;
  for (int i = -1; i <= 1; i++) {
    float cellOffset = float(i);
    float pointPosition = cellOffset + hash_float_to_float(cellPosition + cellOffset) * randomness;
    float distanceToPoint = voronoi_distance1D(pointPosition, localPosition, metric, exponent);
    if (distanceToPoint < minDistance) {
      targetOffset = cellOffset;
      minDistance = distanceToPoint;
      targetPosition = pointPosition;
    }
  }
  outDistance = minDistance;
  outColor.xyz = hash_float_to_vec3(cellPosition + targetOffset);
  outColor.w = 1.0;
  outW = float_divide(targetPosition + cellPosition, scale);
}

void voronoi_texture_smooth_f1_1d(
                                    float w,
                                    float scale,
                                    float smoothness,
                                    float exponent,
                                    float randomness,
                                    float metric,
                                    out float outDistance,
                                    out vec4 outColor,
                                    out vec3 outPosition,
                                    out float outW,
                                    out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);
  smoothness = clamp(smoothness / 2.0, 0.0, 0.5);

  float scaledCoord = w * scale;
  float cellPosition = floor(scaledCoord);
  float localPosition = scaledCoord - cellPosition;

  float smoothDistance = 8.0;
  float smoothPosition = 0.0;
  vec3 smoothColor = vec3(0.0);
  for (int i = -2; i <= 2; i++) {
    float cellOffset = float(i);
    float pointPosition = cellOffset + hash_float_to_float(cellPosition + cellOffset) * randomness;
    float distanceToPoint = voronoi_distance1D(pointPosition, localPosition, metric, exponent);
    float h = smoothstep(0.0, 1.0, 0.5 + 0.5 * (smoothDistance - distanceToPoint) / smoothness);
    float correctionFactor = smoothness * h * (1.0 - h);
    smoothDistance = mix(smoothDistance, distanceToPoint, h) - correctionFactor;
    correctionFactor /= 1.0 + 3.0 * smoothness;
    vec3 cellColor = hash_float_to_vec3(cellPosition + cellOffset);
    smoothColor = mix(smoothColor, cellColor, h) - correctionFactor;
    smoothPosition = mix(smoothPosition, pointPosition, h) - correctionFactor;
  }
  outDistance = smoothDistance;
  outColor.xyz = smoothColor;
  outColor.w = 1.0;
  outW = float_divide(cellPosition + smoothPosition, scale);
}

void voronoi_texture_f2_1d(
                            float w,
                            float scale,
                            float smoothness,
                            float exponent,
                            float randomness,
                            float metric,
                            out float outDistance,
                            out vec4 outColor,
                            out vec3 outPosition,
                            out float outW,
                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  float scaledCoord = w * scale;
  float cellPosition = floor(scaledCoord);
  float localPosition = scaledCoord - cellPosition;

  float distanceF1 = 8.0;
  float distanceF2 = 8.0;
  float offsetF1 = 0.0;
  float positionF1 = 0.0;
  float offsetF2, positionF2;
  for (int i = -1; i <= 1; i++) {
    float cellOffset = float(i);
    float pointPosition = cellOffset + hash_float_to_float(cellPosition + cellOffset) * randomness;
    float distanceToPoint = voronoi_distance1D(pointPosition, localPosition, metric, exponent);
    if (distanceToPoint < distanceF1) {
      distanceF2 = distanceF1;
      distanceF1 = distanceToPoint;
      offsetF2 = offsetF1;
      offsetF1 = cellOffset;
      positionF2 = positionF1;
      positionF1 = pointPosition;
    }
    else if (distanceToPoint < distanceF2) {
      distanceF2 = distanceToPoint;
      offsetF2 = cellOffset;
      positionF2 = pointPosition;
    }
  }
  outDistance = distanceF2;
  outColor.xyz = hash_float_to_vec3(cellPosition + offsetF2);
  outColor.w = 1.0;
  outW = float_divide(positionF2 + cellPosition, scale);
}

void voronoi_texture_distance_to_edge_1d(
                                            float w,
                                            float scale,
                                            float smoothness,
                                            float exponent,
                                            float randomness,
                                            float metric,
                                            out float outDistance,
                                            out vec4 outColor,
                                            out vec3 outPosition,
                                            out float outW,
                                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  float scaledCoord = w * scale;
  float cellPosition = floor(scaledCoord);
  float localPosition = scaledCoord - cellPosition;

  float midPointPosition = hash_float_to_float(cellPosition) * randomness;
  float leftPointPosition = -1.0 + hash_float_to_float(cellPosition - 1.0) * randomness;
  float rightPointPosition = 1.0 + hash_float_to_float(cellPosition + 1.0) * randomness;
  float distanceToMidLeft = distance((midPointPosition + leftPointPosition) / 2.0, localPosition);
  float distanceToMidRight = distance((midPointPosition + rightPointPosition) / 2.0,
                                      localPosition);

  outDistance = min(distanceToMidLeft, distanceToMidRight);
}

void voronoi_texture_n_sphere_radius_1d(
                                            float w,
                                            float scale,
                                            float smoothness,
                                            float exponent,
                                            float randomness,
                                            float metric,
                                            out float outDistance,
                                            out vec4 outColor,
                                            out vec3 outPosition,
                                            out float outW,
                                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  float scaledCoord = w * scale;
  float cellPosition = floor(scaledCoord);
  float localPosition = scaledCoord - cellPosition;

  float closestPoint;
  float closestPointOffset;
  float minDistance = 8.0;
  for (int i = -1; i <= 1; i++) {
    float cellOffset = float(i);
    float pointPosition = cellOffset + hash_float_to_float(cellPosition + cellOffset) * randomness;
    float distanceToPoint = distance(pointPosition, localPosition);
    if (distanceToPoint < minDistance) {
      minDistance = distanceToPoint;
      closestPoint = pointPosition;
      closestPointOffset = cellOffset;
    }
  }

  minDistance = 8.0;
  float closestPointToClosestPoint;
  for (int i = -1; i <= 1; i++) {
    if (i == 0) {
      continue;
    }
    float cellOffset = float(i) + closestPointOffset;
    float pointPosition = cellOffset + hash_float_to_float(cellPosition + cellOffset) * randomness;
    float distanceToPoint = distance(closestPoint, pointPosition);
    if (distanceToPoint < minDistance) {
      minDistance = distanceToPoint;
      closestPointToClosestPoint = pointPosition;
    }
  }
  outRadius = distance(closestPointToClosestPoint, closestPoint) / 2.0;
}

// VORONOI 2D

void voronoi_texture_f1_2d( vec2 coord,
                            float scale,
                            float smoothness,
                            float exponent,
                            float randomness,
                            float metric,
                            out float outDistance,
                            out vec4 outColor,
                            out vec3 outPosition,
                            out float outW,
                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec2 scaledCoord = coord.xy * scale;
  vec2 cellPosition = floor(scaledCoord);
  vec2 localPosition = scaledCoord - cellPosition;

  float minDistance = 8.0;
  vec2 targetOffset, targetPosition;
  for (int j = -1; j <= 1; j++) {
    for (int i = -1; i <= 1; i++) {
      vec2 cellOffset = vec2(i, j);
      vec2 pointPosition = cellOffset + hash_vec2_to_vec2(cellPosition + cellOffset) * randomness;
      float distanceToPoint = voronoi_distance2D(pointPosition, localPosition, metric, exponent);
      if (distanceToPoint < minDistance) {
        targetOffset = cellOffset;
        minDistance = distanceToPoint;
        targetPosition = pointPosition;
      }
    }
  }
  outDistance = minDistance;
  outColor.xyz = hash_vec2_to_vec3(cellPosition + targetOffset);
  outColor.w = 1.0;
  outPosition = vec3(vec2_divide(targetPosition + cellPosition, vec2(scale)), 0.0);
}

void voronoi_texture_smooth_f1_2d(  vec2 coord,
                                    float scale,
                                    float smoothness,
                                    float exponent,
                                    float randomness,
                                    float metric,
                                    out float outDistance,
                                    out vec4 outColor,
                                    out vec3 outPosition,
                                    out float outW,
                                    out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);
  smoothness = clamp(smoothness / 2.0, 0.0, 0.5);

  vec2 scaledCoord = coord.xy * scale;
  vec2 cellPosition = floor(scaledCoord);
  vec2 localPosition = scaledCoord - cellPosition;

  float smoothDistance = 8.0;
  vec3 smoothColor = vec3(0.0);
  vec2 smoothPosition = vec2(0.0);
  for (int j = -2; j <= 2; j++) {
    for (int i = -2; i <= 2; i++) {
      vec2 cellOffset = vec2(i, j);
      vec2 pointPosition = cellOffset + hash_vec2_to_vec2(cellPosition + cellOffset) * randomness;
      float distanceToPoint = voronoi_distance2D(pointPosition, localPosition, metric, exponent);
      float h = smoothstep(0.0, 1.0, 0.5 + 0.5 * (smoothDistance - distanceToPoint) / smoothness);
      float correctionFactor = smoothness * h * (1.0 - h);
      smoothDistance = mix(smoothDistance, distanceToPoint, h) - correctionFactor;
      correctionFactor /= 1.0 + 3.0 * smoothness;
      vec3 cellColor = hash_vec2_to_vec3(cellPosition + cellOffset);
      smoothColor = mix(smoothColor, cellColor, h) - correctionFactor;
      smoothPosition = mix(smoothPosition, pointPosition, h) - correctionFactor;
    }
  }
  outDistance = smoothDistance;
  outColor.xyz = smoothColor;
  outColor.w = 1.0;
  outPosition = vec3(vec2_divide(cellPosition + smoothPosition, vec2(scale)), 0.0);
}

void voronoi_texture_f2_2d( vec2 coord,
                            float scale,
                            float smoothness,
                            float exponent,
                            float randomness,
                            float metric,
                            out float outDistance,
                            out vec4 outColor,
                            out vec3 outPosition,
                            out float outW,
                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec2 scaledCoord = coord.xy * scale;
  vec2 cellPosition = floor(scaledCoord);
  vec2 localPosition = scaledCoord - cellPosition;

  float distanceF1 = 8.0;
  float distanceF2 = 8.0;
  vec2 offsetF1 = vec2(0.0);
  vec2 positionF1 = vec2(0.0);
  vec2 offsetF2, positionF2;
  for (int j = -1; j <= 1; j++) {
    for (int i = -1; i <= 1; i++) {
      vec2 cellOffset = vec2(i, j);
      vec2 pointPosition = cellOffset + hash_vec2_to_vec2(cellPosition + cellOffset) * randomness;
      float distanceToPoint = voronoi_distance2D(pointPosition, localPosition, metric, exponent);
      if (distanceToPoint < distanceF1) {
        distanceF2 = distanceF1;
        distanceF1 = distanceToPoint;
        offsetF2 = offsetF1;
        offsetF1 = cellOffset;
        positionF2 = positionF1;
        positionF1 = pointPosition;
      }
      else if (distanceToPoint < distanceF2) {
        distanceF2 = distanceToPoint;
        offsetF2 = cellOffset;
        positionF2 = pointPosition;
      }
    }
  }
  outDistance = distanceF2;
  outColor.xyz = hash_vec2_to_vec3(cellPosition + offsetF2);
  outColor.w = 1.0;
  outPosition = vec3(vec2_divide(positionF2 + cellPosition, vec2(scale)), 0.0);
}

void voronoi_texture_distance_to_edge_2d(   vec2 coord,
                                            float scale,
                                            float smoothness,
                                            float exponent,
                                            float randomness,
                                            float metric,
                                            out float outDistance,
                                            out vec4 outColor,
                                            out vec3 outPosition,
                                            out float outW,
                                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec2 scaledCoord = coord.xy * scale;
  vec2 cellPosition = floor(scaledCoord);
  vec2 localPosition = scaledCoord - cellPosition;

  vec2 vectorToClosest;
  float minDistance = 8.0;
  for (int j = -1; j <= 1; j++) {
    for (int i = -1; i <= 1; i++) {
      vec2 cellOffset = vec2(i, j);
      vec2 vectorToPoint = cellOffset + hash_vec2_to_vec2(cellPosition + cellOffset) * randomness -
                           localPosition;
      float distanceToPoint = dot(vectorToPoint, vectorToPoint);
      if (distanceToPoint < minDistance) {
        minDistance = distanceToPoint;
        vectorToClosest = vectorToPoint;
      }
    }
  }

  minDistance = 8.0;
  for (int j = -1; j <= 1; j++) {
    for (int i = -1; i <= 1; i++) {
      vec2 cellOffset = vec2(i, j);
      vec2 vectorToPoint = cellOffset + hash_vec2_to_vec2(cellPosition + cellOffset) * randomness -
                           localPosition;
      vec2 perpendicularToEdge = vectorToPoint - vectorToClosest;
      if (dot(perpendicularToEdge, perpendicularToEdge) > 0.0001) {
        float distanceToEdge = dot((vectorToClosest + vectorToPoint) / 2.0,
                                   normalize(perpendicularToEdge));
        minDistance = min(minDistance, distanceToEdge);
      }
    }
  }
  outDistance = minDistance;
}

void voronoi_texture_n_sphere_radius_2d(vec2 coord,
                                        float scale,
                                        float smoothness,
                                        float exponent,
                                        float randomness,
                                        float metric,
                                        out float outDistance,
                                        out vec4 outColor,
                                        out vec3 outPosition,
                                        out float outW,
                                        out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec2 scaledCoord = coord.xy * scale;
  vec2 cellPosition = floor(scaledCoord);
  vec2 localPosition = scaledCoord - cellPosition;

  vec2 closestPoint;
  vec2 closestPointOffset;
  float minDistance = 8.0;
  for (int j = -1; j <= 1; j++) {
    for (int i = -1; i <= 1; i++) {
      vec2 cellOffset = vec2(i, j);
      vec2 pointPosition = cellOffset + hash_vec2_to_vec2(cellPosition + cellOffset) * randomness;
      float distanceToPoint = distance(pointPosition, localPosition);
      if (distanceToPoint < minDistance) {
        minDistance = distanceToPoint;
        closestPoint = pointPosition;
        closestPointOffset = cellOffset;
      }
    }
  }

  minDistance = 8.0;
  vec2 closestPointToClosestPoint;
  for (int j = -1; j <= 1; j++) {
    for (int i = -1; i <= 1; i++) {
      if (i == 0 && j == 0) {
        continue;
      }
      vec2 cellOffset = vec2(i, j) + closestPointOffset;
      vec2 pointPosition = cellOffset + hash_vec2_to_vec2(cellPosition + cellOffset) * randomness;
      float distanceToPoint = distance(closestPoint, pointPosition);
      if (distanceToPoint < minDistance) {
        minDistance = distanceToPoint;
        closestPointToClosestPoint = pointPosition;
      }
    }
  }
  outRadius = distance(closestPointToClosestPoint, closestPoint) / 2.0;
}

// 3D VORONOI

void voronoi_texture_f1_3d(vec3 coord,
                            float scale,
                            float smoothness,
                            float exponent,
                            float randomness,
                            float metric,
                            out float outDistance,
                            out vec4 outColor,
                            out vec3 outPosition,
                            out float outW,
                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec3 scaledCoord = coord * scale;
  vec3 cellPosition = floor(scaledCoord);
  vec3 localPosition = scaledCoord - cellPosition;

  float minDistance = 8.0;
  vec3 targetOffset, targetPosition;
  for (int k = -1; k <= 1; k++) {
    for (int j = -1; j <= 1; j++) {
      for (int i = -1; i <= 1; i++) {
        vec3 cellOffset = vec3(i, j, k);
        vec3 pointPosition = cellOffset +
                             hash_vec3_to_vec3(cellPosition + cellOffset) * randomness;
        float distanceToPoint = voronoi_distance(pointPosition, localPosition, metric, exponent);
        if (distanceToPoint < minDistance) {
          targetOffset = cellOffset;
          minDistance = distanceToPoint;
          targetPosition = pointPosition;
        }
      }
    }
  }
  outDistance = minDistance;
  outColor.xyz = hash_vec3_to_vec3(cellPosition + targetOffset);
  outColor.w = 1.0;
  outPosition = vec3_divide(targetPosition + cellPosition, vec3(scale));
}

void voronoi_texture_smooth_f1_3d(vec3 coord,
                                   float scale,
                                   float smoothness,
                                   float exponent,
                                   float randomness,
                                   float metric,
                                   out float outDistance,
                                   out vec4 outColor,
                                   out vec3 outPosition,
                                   out float outW,
                                   out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);
  smoothness = clamp(smoothness / 2.0, 0.0, 0.5);

  vec3 scaledCoord = coord * scale;
  vec3 cellPosition = floor(scaledCoord);
  vec3 localPosition = scaledCoord - cellPosition;

  float smoothDistance = 8.0;
  vec3 smoothColor = vec3(0.0);
  vec3 smoothPosition = vec3(0.0);
  for (int k = -2; k <= 2; k++) {
    for (int j = -2; j <= 2; j++) {
      for (int i = -2; i <= 2; i++) {
        vec3 cellOffset = vec3(i, j, k);
        vec3 pointPosition = cellOffset +
                             hash_vec3_to_vec3(cellPosition + cellOffset) * randomness;
        float distanceToPoint = voronoi_distance(pointPosition, localPosition, metric, exponent);
        float h = smoothstep(
            0.0, 1.0, 0.5 + 0.5 * (smoothDistance - distanceToPoint) / smoothness);
        float correctionFactor = smoothness * h * (1.0 - h);
        smoothDistance = mix(smoothDistance, distanceToPoint, h) - correctionFactor;
        correctionFactor /= 1.0 + 3.0 * smoothness;
        vec3 cellColor = hash_vec3_to_vec3(cellPosition + cellOffset);
        smoothColor = mix(smoothColor, cellColor, h) - correctionFactor;
        smoothPosition = mix(smoothPosition, pointPosition, h) - correctionFactor;
      }
    }
  }
  outDistance = smoothDistance;
  outColor.xyz = smoothColor;
  outColor.w = 1.0;
  outPosition = vec3_divide(cellPosition + smoothPosition, vec3(scale));
}

void voronoi_texture_f2_3d(vec3 coord,
                            float scale,
                            float smoothness,
                            float exponent,
                            float randomness,
                            float metric,
                            out float outDistance,
                            out vec4 outColor,
                            out vec3 outPosition,
                            out float outW,
                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec3 scaledCoord = coord * scale;
  vec3 cellPosition = floor(scaledCoord);
  vec3 localPosition = scaledCoord - cellPosition;

  float distanceF1 = 8.0;
  float distanceF2 = 8.0;
  vec3 offsetF1 = vec3(0.0);
  vec3 positionF1 = vec3(0.0);
  vec3 offsetF2, positionF2;
  for (int k = -1; k <= 1; k++) {
    for (int j = -1; j <= 1; j++) {
      for (int i = -1; i <= 1; i++) {
        vec3 cellOffset = vec3(i, j, k);
        vec3 pointPosition = cellOffset +
                             hash_vec3_to_vec3(cellPosition + cellOffset) * randomness;
        float distanceToPoint = voronoi_distance(pointPosition, localPosition, metric, exponent);
        if (distanceToPoint < distanceF1) {
          distanceF2 = distanceF1;
          distanceF1 = distanceToPoint;
          offsetF2 = offsetF1;
          offsetF1 = cellOffset;
          positionF2 = positionF1;
          positionF1 = pointPosition;
        }
        else if (distanceToPoint < distanceF2) {
          distanceF2 = distanceToPoint;
          offsetF2 = cellOffset;
          positionF2 = pointPosition;
        }
      }
    }
  }
  outDistance = distanceF2;
  outColor.xyz = hash_vec3_to_vec3(cellPosition + offsetF2);
  outColor.w = 1.0;
  outPosition = vec3_divide(positionF2 + cellPosition, vec3(scale));
}

void voronoi_texture_distance_to_edge_3d(vec3 coord,
                                          float scale,
                                          float smoothness,
                                          float exponent,
                                          float randomness,
                                          float metric,
                                          out float outDistance,
                                          out vec4 outColor,
                                          out vec3 outPosition,
                                          out float outW,
                                          out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec3 scaledCoord = coord * scale;
  vec3 cellPosition = floor(scaledCoord);
  vec3 localPosition = scaledCoord - cellPosition;

  vec3 vectorToClosest;
  float minDistance = 8.0;
  for (int k = -1; k <= 1; k++) {
    for (int j = -1; j <= 1; j++) {
      for (int i = -1; i <= 1; i++) {
        vec3 cellOffset = vec3(i, j, k);
        vec3 vectorToPoint = cellOffset +
                             hash_vec3_to_vec3(cellPosition + cellOffset) * randomness -
                             localPosition;
        float distanceToPoint = dot(vectorToPoint, vectorToPoint);
        if (distanceToPoint < minDistance) {
          minDistance = distanceToPoint;
          vectorToClosest = vectorToPoint;
        }
      }
    }
  }

  minDistance = 8.0;
  for (int k = -1; k <= 1; k++) {
    for (int j = -1; j <= 1; j++) {
      for (int i = -1; i <= 1; i++) {
        vec3 cellOffset = vec3(i, j, k);
        vec3 vectorToPoint = cellOffset +
                             hash_vec3_to_vec3(cellPosition + cellOffset) * randomness -
                             localPosition;
        vec3 perpendicularToEdge = vectorToPoint - vectorToClosest;
        if (dot(perpendicularToEdge, perpendicularToEdge) > 0.0001) {
          float distanceToEdge = dot((vectorToClosest + vectorToPoint) / 2.0,
                                     normalize(perpendicularToEdge));
          minDistance = min(minDistance, distanceToEdge);
        }
      }
    }
  }
  outDistance = minDistance;
}

void voronoi_texture_n_sphere_radius_3d(vec3 coord,
                                         float scale,
                                         float smoothness,
                                         float exponent,
                                         float randomness,
                                         float metric,
                                         out float outDistance,
                                         out vec4 outColor,
                                         out vec3 outPosition,
                                         out float outW,
                                         out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec3 scaledCoord = coord * scale;
  vec3 cellPosition = floor(scaledCoord);
  vec3 localPosition = scaledCoord - cellPosition;

  vec3 closestPoint;
  vec3 closestPointOffset;
  float minDistance = 8.0;
  for (int k = -1; k <= 1; k++) {
    for (int j = -1; j <= 1; j++) {
      for (int i = -1; i <= 1; i++) {
        vec3 cellOffset = vec3(i, j, k);
        vec3 pointPosition = cellOffset +
                             hash_vec3_to_vec3(cellPosition + cellOffset) * randomness;
        float distanceToPoint = distance(pointPosition, localPosition);
        if (distanceToPoint < minDistance) {
          minDistance = distanceToPoint;
          closestPoint = pointPosition;
          closestPointOffset = cellOffset;
        }
      }
    }
  }

  minDistance = 8.0;
  vec3 closestPointToClosestPoint;
  for (int k = -1; k <= 1; k++) {
    for (int j = -1; j <= 1; j++) {
      for (int i = -1; i <= 1; i++) {
        if (i == 0 && j == 0 && k == 0) {
          continue;
        }
        vec3 cellOffset = vec3(i, j, k) + closestPointOffset;
        vec3 pointPosition = cellOffset +
                             hash_vec3_to_vec3(cellPosition + cellOffset) * randomness;
        float distanceToPoint = distance(closestPoint, pointPosition);
        if (distanceToPoint < minDistance) {
          minDistance = distanceToPoint;
          closestPointToClosestPoint = pointPosition;
        }
      }
    }
  }
  outRadius = distance(closestPointToClosestPoint, closestPoint) / 2.0;
}

// 4D VORONOI

void voronoi_texture_f1_4d(vec4 coord,
                            float scale,
                            float smoothness,
                            float exponent,
                            float randomness,
                            float metric,
                            out float outDistance,
                            out vec4 outColor,
                            out vec3 outPosition,
                            out float outW,
                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec4 scaledCoord = coord * scale;
  vec4 cellPosition = floor(scaledCoord);
  vec4 localPosition = scaledCoord - cellPosition;

  float minDistance = 8.0;
  vec4 targetOffset, targetPosition;
  for (int u = -1; u <= 1; u++) {
    for (int k = -1; k <= 1; k++) {
      for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
          vec4 cellOffset = vec4(i, j, k, u);
          vec4 pointPosition = cellOffset +
                               hash_vec4_to_vec4(cellPosition + cellOffset) * randomness;
          float distanceToPoint = voronoi_distance(pointPosition, localPosition, metric, exponent);
          if (distanceToPoint < minDistance) {
            targetOffset = cellOffset;
            minDistance = distanceToPoint;
            targetPosition = pointPosition;
          }
        }
      }
    }
  }
  outDistance = minDistance;
  outColor.xyz = hash_vec4_to_vec3(cellPosition + targetOffset);
  outColor.w = 1.0;
  vec4 p = vec4_divide(targetPosition + cellPosition, vec4(scale));
  outPosition = p.xyz;
  outW = p.w;
}

void voronoi_texture_smooth_f1_4d(vec4 coord,
                                   float scale,
                                   float smoothness,
                                   float exponent,
                                   float randomness,
                                   float metric,
                                   out float outDistance,
                                   out vec4 outColor,
                                   out vec3 outPosition,
                                   out float outW,
                                   out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);
  smoothness = clamp(smoothness / 2.0, 0.0, 0.5);

  vec4 scaledCoord = coord * scale;
  vec4 cellPosition = floor(scaledCoord);
  vec4 localPosition = scaledCoord - cellPosition;

  float smoothDistance = 8.0;
  vec3 smoothColor = vec3(0.0);
  vec4 smoothPosition = vec4(0.0);
  for (int u = -2; u <= 2; u++) {
    for (int k = -2; k <= 2; k++) {
      for (int j = -2; j <= 2; j++) {
        for (int i = -2; i <= 2; i++) {
          vec4 cellOffset = vec4(i, j, k, u);
          vec4 pointPosition = cellOffset +
                               hash_vec4_to_vec4(cellPosition + cellOffset) * randomness;
          float distanceToPoint = voronoi_distance(pointPosition, localPosition, metric, exponent);
          float h = smoothstep(
              0.0, 1.0, 0.5 + 0.5 * (smoothDistance - distanceToPoint) / smoothness);
          float correctionFactor = smoothness * h * (1.0 - h);
          smoothDistance = mix(smoothDistance, distanceToPoint, h) - correctionFactor;
          correctionFactor /= 1.0 + 3.0 * smoothness;
          vec3 cellColor = hash_vec4_to_vec3(cellPosition + cellOffset);
          smoothColor = mix(smoothColor, cellColor, h) - correctionFactor;
          smoothPosition = mix(smoothPosition, pointPosition, h) - correctionFactor;
        }
      }
    }
  }
  outDistance = smoothDistance;
  outColor.xyz = smoothColor;
  outColor.w = 1.0;
  vec4 p = vec4_divide(cellPosition + smoothPosition, vec4(scale));
  outPosition = p.xyz;
  outW = p.w;
}

void voronoi_texture_f2_4d(vec4 coord,
                            float scale,
                            float smoothness,
                            float exponent,
                            float randomness,
                            float metric,
                            out float outDistance,
                            out vec4 outColor,
                            out vec3 outPosition,
                            out float outW,
                            out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec4 scaledCoord = coord * scale;
  vec4 cellPosition = floor(scaledCoord);
  vec4 localPosition = scaledCoord - cellPosition;

  float distanceF1 = 8.0;
  float distanceF2 = 8.0;
  vec4 offsetF1 = vec4(0.0);
  vec4 positionF1 = vec4(0.0);
  vec4 offsetF2, positionF2;
  for (int u = -1; u <= 1; u++) {
    for (int k = -1; k <= 1; k++) {
      for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
          vec4 cellOffset = vec4(i, j, k, u);
          vec4 pointPosition = cellOffset +
                               hash_vec4_to_vec4(cellPosition + cellOffset) * randomness;
          float distanceToPoint = voronoi_distance(pointPosition, localPosition, metric, exponent);
          if (distanceToPoint < distanceF1) {
            distanceF2 = distanceF1;
            distanceF1 = distanceToPoint;
            offsetF2 = offsetF1;
            offsetF1 = cellOffset;
            positionF2 = positionF1;
            positionF1 = pointPosition;
          }
          else if (distanceToPoint < distanceF2) {
            distanceF2 = distanceToPoint;
            offsetF2 = cellOffset;
            positionF2 = pointPosition;
          }
        }
      }
    }
  }
  outDistance = distanceF2;
  outColor.xyz = hash_vec4_to_vec3(cellPosition + offsetF2);
  outColor.w = 1.0;
  vec4 p = vec4_divide(positionF2 + cellPosition, vec4(scale));
  outPosition = p.xyz;
  outW = p.w;
}

void voronoi_texture_distance_to_edge_4d(vec4 coord,
                                          float scale,
                                          float smoothness,
                                          float exponent,
                                          float randomness,
                                          float metric,
                                          out float outDistance,
                                          out vec4 outColor,
                                          out vec3 outPosition,
                                          out float outW,
                                          out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec4 scaledCoord = coord * scale;
  vec4 cellPosition = floor(scaledCoord);
  vec4 localPosition = scaledCoord - cellPosition;

  vec4 vectorToClosest;
  float minDistance = 8.0;
  for (int u = -1; u <= 1; u++) {
    for (int k = -1; k <= 1; k++) {
      for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
          vec4 cellOffset = vec4(i, j, k, u);
          vec4 vectorToPoint = cellOffset +
                               hash_vec4_to_vec4(cellPosition + cellOffset) * randomness -
                               localPosition;
          float distanceToPoint = dot(vectorToPoint, vectorToPoint);
          if (distanceToPoint < minDistance) {
            minDistance = distanceToPoint;
            vectorToClosest = vectorToPoint;
          }
        }
      }
    }
  }

  minDistance = 8.0;
  for (int u = -1; u <= 1; u++) {
    for (int k = -1; k <= 1; k++) {
      for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
          vec4 cellOffset = vec4(i, j, k, u);
          vec4 vectorToPoint = cellOffset +
                               hash_vec4_to_vec4(cellPosition + cellOffset) * randomness -
                               localPosition;
          vec4 perpendicularToEdge = vectorToPoint - vectorToClosest;
          if (dot(perpendicularToEdge, perpendicularToEdge) > 0.0001) {
            float distanceToEdge = dot((vectorToClosest + vectorToPoint) / 2.0,
                                       normalize(perpendicularToEdge));
            minDistance = min(minDistance, distanceToEdge);
          }
        }
      }
    }
  }
  outDistance = minDistance;
}

void voronoi_texture_n_sphere_radius_4d(vec4 coord,
                                         float scale,
                                         float smoothness,
                                         float exponent,
                                         float randomness,
                                         float metric,
                                         out float outDistance,
                                         out vec4 outColor,
                                         out vec3 outPosition,
                                         out float outW,
                                         out float outRadius){
  randomness = clamp(randomness, 0.0, 1.0);

  vec4 scaledCoord = coord * scale;
  vec4 cellPosition = floor(scaledCoord);
  vec4 localPosition = scaledCoord - cellPosition;

  vec4 closestPoint;
  vec4 closestPointOffset;
  float minDistance = 8.0;
  for (int u = -1; u <= 1; u++) {
    for (int k = -1; k <= 1; k++) {
      for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
          vec4 cellOffset = vec4(i, j, k, u);
          vec4 pointPosition = cellOffset +
                               hash_vec4_to_vec4(cellPosition + cellOffset) * randomness;
          float distanceToPoint = distance(pointPosition, localPosition);
          if (distanceToPoint < minDistance) {
            minDistance = distanceToPoint;
            closestPoint = pointPosition;
            closestPointOffset = cellOffset;
          }
        }
      }
    }
  }

  minDistance = 8.0;
  vec4 closestPointToClosestPoint;
  for (int u = -1; u <= 1; u++) {
    for (int k = -1; k <= 1; k++) {
      for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
          if (i == 0 && j == 0 && k == 0 && u == 0) {
            continue;
          }
          vec4 cellOffset = vec4(i, j, k, u) + closestPointOffset;
          vec4 pointPosition = cellOffset +
                               hash_vec4_to_vec4(cellPosition + cellOffset) * randomness;
          float distanceToPoint = distance(closestPoint, pointPosition);
          if (distanceToPoint < minDistance) {
            minDistance = distanceToPoint;
            closestPointToClosestPoint = pointPosition;
          }
        }
      }
    }
  }
  outRadius = distance(closestPointToClosestPoint, closestPoint) / 2.0;
}

vec4 sampler2D_sample_environment( sampler2D texture, vec3 vector ){
    vec2 uv = hdri_uv( vector );
    return sampler2D_sample_nearest( texture, uv );
}

/* META
    @normal: default = NORMAL;
    @roughness: default = 0.0;
    @samples: default = 1;
*/
vec4 sampler2D_sample_environment_blurry( sampler2D texture, vec3 normal, float roughness, int samples ){
    samples = clamp( samples, 1, 1024 );
    roughness = clamp( roughness * 0.5, 0.0, 0.5 );
    vec3 incoming = incoming_vector( );
    vec4 result;
    for( int i = 0; i < samples; i++ ){
        vec3 diffuse_normal = mix( normal, hash( normal + random_vec3_offset( i ) ).xyz - vec3( 0.5 ), roughness );
        vec3 reflection_vector = reflect( incoming, normalize( diffuse_normal ));
        result += sampler2D_sample_environment( texture, reflection_vector );
    }
    return result / samples;
}

vec4 texture_flow( sampler2D texture, vec2 uv, vec2 flow, float progression, int samples ){
  vec4 result;
  float fraction = 1.0 / float( samples );
  for( int i = 0; i < samples; i++ ){
    float flow_scale = fract( progression - i * fraction );
    vec4 color = sampler2D_sample( texture, uv - flow * vec2( flow_scale ));

    float range = fract( progression - ( float( i ) / samples )) * samples;
    float pingpong;
    math_pingpong( range, 1.0, 0, pingpong );
    float bounds = ( range > 0 && range < 2.0 ) ? 1.0 : 0.0;
    result += color * pingpong * bounds;
  }
  return result;
}

float texture_wave_sine( float mapping, float scale, float phase ){
  mapping = mapping * scale * PI * 2 + phase;
  return sin( mapping - PI / 2 ) * 0.5 + 0.5;
}
float texture_wave_saw( float mapping, float scale, float phase ){
  mapping = mapping * scale + phase;
  return fract( mapping );
}
float texture_wave_triangle( float mapping, float scale, float phase ){
  mapping = mapping * scale + phase;
  float result = fract( mapping ) - 0.5;
  result = 1 - ( abs( result ) * 2 );
  return result;
}

float texture_gradient_linear( float mapping ){
  return clamp( mapping, 0.0, 1.0 );
}
float texture_gradient_quadratic( float mapping ){
  return clamp( mapping * mapping, 0.0, 1.0 );
}
float texture_gradient_easing( float mapping ){
  float r = clamp( mapping, 0.0, 1.0 );
  float t = r * r;
  return ( 3.0 * t - 2.0 * t * r );
}
float texture_gradient_diagonal( vec2 uv ){
  return ( uv.x + uv.y ) * 0.5;
}
float texture_gradient_spherical( vec3 vector ){
  float r = max( 0.9999999 - sqrt( vector.x * vector.x + vector.y * vector.y + vector.z + vector.z ), 0.0 );
  return r;
}
float texture_gradient_quadratic_sphere( vec3 vector ){
  float r = max( 0.9999999 - sqrt( vector.x * vector.x + vector.y * vector.y + vector.z + vector.z ), 0.0 );
  return r * r;
}
float texture_gradient_radial( vec2 uv ){
  return atan( uv.y, uv.x ) / ( PI * 2 ) + 0.5;
}

vec4 texture_white_noise_1d( float w ){
  vec3 vector = hash_float_to_vec3( w );
  float value = hash_vec2_to_float( vec2( w, 1.0 ));
  return vec4( vector, value );
}
vec4 texture_white_noise_2d( vec2 uv ){
  vec3 vector = hash_vec2_to_vec3( uv );
  float value = hash_vec3_to_float( vec3( uv, 2.0 ));
  return vec4( vector, value );
}
vec4 texture_white_noise_3d( vec3 vector ){
  vec3 out_vector =  hash_vec3_to_vec3( vector );
  float value = hash_vec4_to_float( vec4( vector, 3.0 ));
  return vec4( out_vector, value );
}
vec4 texture_white_noise_4d( vec4 color ){
  return hash_vec4_to_vec4( color );
}

#endif