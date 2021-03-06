# Shader Nodes

**Other:**
- EssentialsBackground / EssentialsBackground : [background.py]
- EssentialsBloom / EssentialsBloom : [bloom.py]
- EssentialsClouds / EssentialsClouds : [clouds.py]
- EssentialsDOF / EssentialsDOF : [depth_of_field.py]
- EssentialsDithering / EssentialsDithering : [dithering.py]
- EssentialsLensDistortion / EssentialsLensDistortion : [lens_distortion.py]
- EssentialsLensFlare / EssentialsLensFlare : [lens_flare.py]
- DummyPipelineNode / DummyPipelineNode : [pipeline_node.py]
- EssentialsSky / EssentialsSky : [sky.py]
- EssentialsSunFlare / EssentialsSunFlare : [sun_flare.py]

**Input:**
- Ambient Occlusion / MaltNodeAmbientOcclusion : [nodes/ambient_occlusion.py]
- Curve View Mapping / MaltNodeCurveViewMapping : [nodes/curve_view_mapping.py]
- Geometry / MaltNodeGeometry : [nodes/geometry.py]
- Interior Mapping / MaltNodeInteriorMapping : [nodes/interior_mapping.py]
- Layer Weight / MaltNodeLayerWeight : [nodes/layer_weight.py]
- Matrices / MaltNodeMatrices : [nodes/matrices.py]
- Object Data / MaltNodeObjectData : [nodes/object_data.py]
- Object Info / MaltNodeObjectInfo : [nodes/object_info.py]
- Parallax Mapping / MaltNodeParallaxMapping : [nodes/parallax_mapping.py]
- Screen Space / MaltNodeScreenSpace : [nodes/screenspace.py]
- Tangent / MaltNodeTangent : [nodes/tangent.py]
- Texture Coordinate / MaltNodeTextureCoordinate : [nodes/texture_coordinate.py]
- UV Map / MaltNodeUVMap : [nodes/texture_coordinate.py]
- Sky Coordinates / MaltNodeSkyCoords : [nodes/texture_coordinate.py]
- Vertex Color / MaltNodeVertexColor : [nodes/vertex_color.py]

**Primitives:**
- Float / MaltNodeFloat : [nodes/primitives.py]
- Int / MaltNodeInt : [nodes/primitives.py]
- Bool / MaltNodeBool : [nodes/primitives.py]
- UV / MaltNodeUV : [nodes/primitives.py]
- Vector / MaltNodeVector : [nodes/primitives.py]
- Color / MaltNodeColor : [nodes/primitives.py]
- Ramp / MaltNodeRamp : [nodes/primitives.py]
- Texture / MaltNodeTexture : [nodes/primitives.py]
- Matrix 3 / MaltNodeMatrix 3 : [nodes/primitives.py]
- Matrix 4 / MaltNodeMatrix 4 : [nodes/primitives.py]

**Shader:**
- Diffuse / MaltNodeDiffuseShader : [nodes/base_shaders.py]
- Specular / MaltNodeSpecularShader : [nodes/base_shaders.py]
- Gradient / MaltNodeGradientShading : [nodes/base_shaders.py]
- Emission / MaltNodeEmission : [nodes/base_shaders.py]
- Toon Shader / MaltNodeToonShader : [nodes/toon_shader.py]

**Color:**
- Bright/Contrast / MaltNodeBrightContrast : [nodes/bright_contrast.py]
- Hue Saturation Value / MaltNodeHueSaturation : [nodes/COLOR_collection.py]
- Gamma / MaltNodeGamma : [nodes/COLOR_collection.py]
- Invert / MaltNodeInvert : [nodes/COLOR_collection.py]
- Color Palette / MaltNodeColorPalette : [nodes/color_palette.py]
- Mix / MaltNodeMixRGB : [nodes/mix_rgb.py]

**Texture:**
- Outlines / MaltNodeOutlines : [nodes/outlines.py]
- Blur / MaltNodeTexBlur : [nodes/tex_blur.py]
- Environment Texture / MaltNodeTexEnvironment : [nodes/tex_environment.py]
- Gradient Texture / MaltNodeTexGradient : [nodes/tex_gradient.py]
- Hexagon Tiles / MaltNodeTexHexTiles : [nodes/tex_hex_tiles.py]
- Image Texture / MaltNodeTexImage : [nodes/tex_image.py]
- Normal Map / MaltNodeNormalMap : [nodes/tex_image.py]
- Noise Texture / MaltNodeTextNoise : [nodes/tex_noise.py]
- Texture Flow / MaltNodeTextureFlow : [nodes/tex_texture_flow.py]
- Voronoi Texture / MaltNodeTexVoronoi : [nodes/tex_voronoi.py]
- Wave Texture / MaltNodeTexWave : [nodes/tex_wave.py]
- White Noise / MaltNodeTexWhiteNoise : [nodes/tex_white_noise.py]

**Convertor:**
- Bayer Dither / MaltNodeBayerDither : [nodes/bayer_dithering.py]
- Clamp / MaltNodeClamp : [nodes/clamp.py]
- Color Ramp / MaltNodeColorRamp : [nodes/color_ramp.py]
- Lerp / MaltNodeLerp : [nodes/lerp.py]
- Map Range / MaltNodeMapRange : [nodes/map_range.py]
- Math / MaltNodeMath : [nodes/math.py]
- Pack / MaltNodePack : [nodes/pack_unpack.py]
- Unpack / MaltNodeUnpack : [nodes/pack_unpack.py]
- Separate / MaltNodeSeparate : [nodes/separate_combine.py]
- Combine / MaltNodeCombine : [nodes/separate_combine.py]
- Separate HSV / MaltNodeSeparateHSV : [nodes/separate_combine.py]
- Combine HSV / MaltNodeCombineHSV : [nodes/separate_combine.py]
- Vector Math / MaltNodeVectorMath : [nodes/vector_math.py]

**Vector:**
- Bevel / MaltNodeBevel : [nodes/bevel.py]
- Mapping / MaltNodeMapping : [nodes/mapping.py]
- Transformation / MaltNodeTransformation : [nodes/matrices.py]
- Vector Angle / MaltNodeVectorAngle : [nodes/vector_angle.py]
- Vector Distortion / MaltNodeVectorDistortion : [nodes/vector_distortion.py]
- Rotate / MaltNodeVectorRotate : [nodes/vector_rotate.py]
- Vector Transform / MaltNodeVectorTransform : [nodes/vector_transform.py]

