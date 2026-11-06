// Golden number spiral (2024-02-11). Pasted by the user on 2026-11-06.
// The closing brace of mainImage was missing at this point in the paste; it is restored here.

// Function to calculate color for the visual effect, including prime-like points and depth modulation
vec3 calculateColor(vec2 uv, float time) {
    // Time-based rotation
    float angle = time * 0.2;
    float cosA = cos(angle);
    float sinA = sin(angle);
    uv = mat2(cosA, -sinA, sinA, cosA) * uv;

    // Spiral pattern parameters
    float goldenAngle = radians(137.508);
    float r = length(uv) * 8.0;
    float theta = atan(uv.y, uv.x);

    // Depth effect simulation
    float z = mod(r, 10.0);
    float phi = mod(theta, 2.0 * 3.14);

    // Prime-like points visualization
    float primeEffect = step(0.5, fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453));
    primeEffect = smoothstep(0.45, 0.55, primeEffect);

    // Determine if the point is odd or even based on the radius
    float oddEvenEffect = mod(r, 2.0); // 0 for even, 1 for odd

    // Apply different color schemes based on the point's type
    vec3 primeColor = mix(vec3(0.9, 1.0, 0.7), vec3(0.1, 0.0, 0.6), abs(sin(z) + cos(phi)));
    vec3 oddColor = vec3(0.7, 0.3, 0.5); // Example odd color
    vec3 evenColor = vec3(0.3, 0.5, 0.7); // Example even color

    // Color modulation based on depth and prime effect
    vec3 col;
    if (primeEffect == 1.0) {
        col = primeColor; // Use prime color for prime-like points
    } else if (oddEvenEffect == 0.0) {
        col = oddColor; // Use odd color for odd points
    } else {
        col = evenColor; // Use even color for even points
    }

    col *= primeEffect * 0.5 + 0.5; // Apply the prime-like effect dimming

    return col;
}

// ACES tone mapping function for color correction and enhancement
vec3 aces_tonemap(vec3 color) {
    mat3 m1 = mat3(
        0.59719, 0.07600, 0.02840,
        0.35458, 0.90834, 0.13383,
        0.04823, 0.01566, 0.83777
    );
    mat3 m2 = mat3(
        1.60475, -0.10208, -0.00327,
        -0.53108,  1.10813, -0.07276,
        -0.07367, -0.00605,  1.07602
    );
    vec3 v = m1 * color;
    vec3 a = v * (v + 0.0245786) - 0.000090537;
    vec3 b = v * (0.983729 * v + 0.4329510) + 0.238081;
    return pow(clamp(m2 * (a / b), 0.0, 1.0), vec3(1.0 / 2.2));
}

// Main image function with supersampling and ACES tone mapping
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec4 accumColor = vec4(0.0);
    vec2 offsets[9] = vec2[](
        vec2(-0.33, -0.33), vec2(0.0, -0.33), vec2(0.33, -0.33),
        vec2(-0.33, 0.0), vec2(0.0, 0.0), vec2(0.33, 0.0),
        vec2(-0.33, 0.33), vec2(0.0, 0.33), vec2(0.33, 0.33)
    );

    for (int i = 0; i < 9; i++) {
        vec2 ssCoord = fragCoord + offsets[i];
        vec2 uv = (ssCoord - 0.5 * iResolution.xy) / iResolution.y;
        uv *= 50.0 * iTime * 0.01;

        vec3 col = calculateColor(uv,(iMouse.x / iResolution.x) * 10.0);
        col = aces_tonemap(col); // Apply ACES tone mapping

        accumColor += vec4(col, 1.0);
    }

    fragColor = accumColor / 9.0; // Average for anti-aliasing effect
}
