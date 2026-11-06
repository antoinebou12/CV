// Warping Mouse (2024-01-23). Pasted by the user on 2026-11-06.
// INCOMPLETE: the paste does not include fbm4, fbm4_2 and fbm6_2 (or the noise they use).
// The structure matches Inigo Quilez's "Warping - procedural 2" domain-warping shader,
// with mouse offsets added to q and o. Note that `ron` is an input parameter, so `on`
// stays vec4(0) in mainImage as written; the original likely declared it `out vec4 ron`.

float func(vec2 q, vec4 ron, vec2 mouse) {
    q += 0.03*sin( vec2(0.27,0.23)*iTime + length(q)*vec2(4.1,4.3));

	vec2 o = fbm4_2( 0.9*q );

    q += mouse * 0.03;

    o += 0.04*sin( vec2(0.12,0.14)*iTime + length(o));

    o += mouse * 0.03;

    vec2 n = fbm6_2( 3.0*o );

	ron = vec4( o, n );

    float f = 0.5 + 0.5*fbm4( 1.8*q + 6.0*n );

    return mix( f, f*f*f*3.5, f*abs(n.x) );
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 p = (2.0*fragCoord-iResolution.xy)/iResolution.y;
    float e = 2.0/iResolution.y;

    vec4 on = vec4(0.0);
    float f = func(p, on, iMouse.xy/iResolution.y);

	vec3 col = vec3(0.0);
    col = mix( vec3(0.2,0.1,0.4), vec3(0.3,0.05,0.05), f );
    col = mix( col, vec3(0.9,0.9,0.9), dot(on.zw,on.zw) );
    col = mix( col, vec3(0.4,0.3,0.3), 0.2 + 0.5*on.y*on.y );
    col = mix( col, vec3(0.0,0.2,0.4), 0.5*smoothstep(1.2,1.3,abs(on.z)+abs(on.w)) );
    col = clamp( col*f*2.0, 0.0, 1.0 );

#if 0
    // gpu derivatives - bad quality, but fast
	vec3 nor = normalize( vec3( dFdx(f)*iResolution.x, 6.0, dFdy(f)*iResolution.y ) );
#else
    // manual derivatives - better quality, but slower
    vec4 kk;
 	vec3 nor = normalize( vec3( func(p+vec2(e,0.0),kk, iMouse.xy/iResolution.y)-f,
                                2.0*e,
                                func(p+vec2(0.0,e),kk, iMouse.xy/iResolution.y)-f ) );
#endif

    vec3 lig = normalize( vec3( 0.9, 0.2, -0.4 ) );
    float dif = clamp( 0.3+0.7*dot( nor, lig ), 0.0, 1.0 );
    vec3 lin = vec3(0.70,0.90,0.95)*(nor.y*0.5+0.5) + vec3(0.15,0.10,0.05)*dif;
    col *= 1.2*lin;
	col = 1.0 - col;
	col = 1.1*col*col;

    fragColor = vec4( col, 1.0 );
}
