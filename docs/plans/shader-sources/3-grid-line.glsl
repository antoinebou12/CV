// Grid Line (2024-02-11). Pasted by the user on 2026-11-06.

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord / iResolution.xy;

    // Adjust grid size based on mouse x position
    float gridSize = 30.0 + 10.0 * (iMouse.x / iResolution.x);

    // Calculate grid lines
    vec2 grid = abs(fract(uv * gridSize - 0.5) - 0.5) / fwidth(uv * gridSize);
    float line = 1.0 - min(grid.x, grid.y);

    // Create a time-varying background color
    vec3 bgCol = 0.5 + 0.5 * cos(iTime + uv.xyx + vec3(0, 2, 4));

    // Mix the line color with the background color based on line presence
    vec3 col = mix(bgCol, vec3(1.0, 0.8, 0.1), line);

    // Output to screen
    fragColor = vec4(col, 1.0);
}
