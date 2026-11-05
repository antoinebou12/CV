# WearBlender: Blender scenes for wear effects

> Example Blender files showing edge wear, scratches, rotated normal maps, flow maps and painted wear with shaders and geometry nodes.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/wearblender/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/wearblender/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/ETSim/WearBlender


## Use cases

Blender example scenes for learning how to fake wear with shaders, geometry nodes and painting.

- **Study an edge-wear shader** (Learner or teacher, Blender 4.5): Edge wear.blend builds a worn-edge mask in the shader editor from Bevel and Geometry nodes, a color ramp and a roughness image texture.
- **Study procedural scratches** (Learner or teacher, Blender 4.5): Scratched.blend combines Voronoi and Noise textures, color ramps and Bump nodes on a Suzanne mesh to draw micro-scratches.
- **Rotate a normal map** (Learner or teacher, Blender 4.5): NormalRotation.blend rotates the vectors of an image-based normal map with Vector Rotate and Vector Math nodes.
- **Drive wear from painted data** (Learner or teacher, Blender 4.5): WeightPainting.blend reads a painted attribute through Named Attribute geometry nodes and an Attribute shader node to mix materials.
- **Offset textures with a flowmap** (Learner or teacher, Blender 4.5): flowmap.blend separates and recombines vector components to push texture coordinates along a flow image.
- **Project a camera texture** (Learner or teacher, Blender 4.5): SurfaceCameraProjection.blend has a second camera, a CameraProjectionMaterial with an emission shader and a rigid-body world.

### Scenario: Take apart the edge-wear scene

1. Clone the repository and open Edge wear.blend in Blender 4.5 LTS.
2. Select the plane and open the Shader Editor to follow the Bevel and Geometry nodes into the color ramp.
3. Change the ramp stops and watch the worn edges grow or shrink in the viewport.
4. Open Scratched.blend and compare how Voronoi and Noise textures feed the Bump node.
5. Copy the node setup into your own material as a starting point.


