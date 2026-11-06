// Sun Ray Clockwise (2024-02-11). Pasted by the user on 2026-11-06.

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Transform the screen coordinate to [-1, 1] range for both axes
    vec2 uv = (fragCoord.xy - 0.5 * iResolution.xy) / iResolution.y;

    // Parameters for the "fake" 3D effect and visualization
    float angle = 360.0;
    float scale = 0.9;
    float offset = iTime * 0.2; // Use time to animate

    // Convert to polar coordinates
    float r = length(uv) * scale;
    float theta = atan(uv.y, uv.x) * degrees(1.0); // Convert to degrees

    // Apply the angle and add time-based animation
    theta += angle * offset;

    // Create a simple pattern based on the angle and distance from center
    float pattern = mod(floor(theta / angle), 2.0);
    pattern *= step(0.5, abs(sin(r - offset) * cos(theta - offset)));

    // Use the pattern to mix colors
    vec3 col = mix(vec3(0.2, 0.3, 0.6), vec3(0.8, 0.7, 0.4), pattern);

    // Output to screen
    fragColor = vec4(col,1.0);
}
