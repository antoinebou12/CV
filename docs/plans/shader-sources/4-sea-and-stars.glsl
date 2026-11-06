// Sea and Stars (2024-01-23). Pasted by the user on 2026-11-06.
// INCOMPLETE: the paste does not define noise, hash, fbm, fromEuler, raySphereIntersect,
// disp, rot, mag2, m3, linstep and iLerp. Their usage matches well-known Shadertoy sources:
// the sea is TDM's "Seascape", the star field in getSkyColor is Kali's "Star Nest", the
// cloud tunnel (mapCloud/renderCloud/disp/rot/m3) is nimitz's "Protean clouds", and the
// sea colour adds the same fbm domain warp as "Domain Wrapping".

const int NUM_STEPS = 8;
const float PI = 3.141592;
const float EPSILON = 1e-3;
#define EPSILON_NRM (0.1 / iResolution.x)

// sea constants
const int ITER_GEOMETRY = 12;
const int ITER_FRAGMENT = 20;
const float SEA_HEIGHT = 0.4;
const float SEA_CHOPPY = 2.0;
const float SEA_SPEED = 0.6;
const float SEA_FREQ = 0.12;
const vec3 SEA_BASE = vec3(0.0, 0.09, 0.18);
const vec3 SEA_WATER_COLOR = vec3(0.8, 0.9, 0.6) * 0.6;
#define SEA_TIME (1.0 + iTime * SEA_SPEED)
const mat2 octave_m = mat2(1.6, 1.2, -1.2, 1.6);

const vec3 SAND_COLOR = vec3(0.9, 0.8, 0.5);

#define iterations 12
#define formuparam 0.53

#define volsteps 20
#define stepsize 0.1

#define zoom   0.800
#define tile   0.850
#define speed  0.5

#define brightness 0.01
#define darkmatter 0.300
#define distfading 0.730
#define saturation 0.850

float prm1 = 0.0;
vec2 bsMo = vec2(0.0);


const vec3 sphereCenters[3] = vec3[3](
    vec3(42.0, -10.0, -70.0),
    vec3(30.0, -10.0, -12.0),
    vec3(0.0, -10.0, 0.0)
);
const float sphereRadii[3] = float[3](6.0, 8.0, 6.0);


// lighting
float diffuse(vec3 n,vec3 l,float p) {
    return pow(dot(n,l) * 0.4 + 0.6,p);
}
float specular(vec3 n,vec3 l,vec3 e,float s) {
    float nrm = (s + 8.0) / (PI * 8.0);
    return pow(max(dot(reflect(e,n),l),0.0),s) * nrm;
}

vec2 mapCloud(vec3 p) {
    vec3 p2 = p;
    p2.xy -= disp(p.z).xy;
    p.xy *= rot(sin(p.z+iTime)*(0.1 + prm1*0.05) + iTime*0.09);
    float cl = mag2(p2.xy);
    float d = 0.;
    p *= .61;
    float z = 1.;
    float trk = 1.;
    float dspAmp = 0.1 + prm1*0.2;
    for(int i = 0; i < 5; i++)
    {
		p += sin(p.zxy*0.75*trk + iTime*trk*.8)*dspAmp;
        d -= abs(dot(cos(p), sin(p.yzx))*z);
        z *= 0.57;
        trk *= 1.4;
        p = p*m3;
    }
    d = abs(d + prm1*3.)+ prm1*.3 - 2.5 + bsMo.y;
    return vec2(d + cl*.2 + 0.25, cl);
}

vec4 renderCloud( in vec3 ro, in vec3 rd, float time )
{
	vec4 rez = vec4(0);
    const float ldst = 8.;
	vec3 lpos = vec3(disp(time + ldst)*0.5, time + ldst);
	float t = 1.5;
	float fogT = 0.;
	for(int i=0; i<130; i++)
	{
		if(rez.a > 0.99)break;

		vec3 pos = ro + t*rd;
        vec2 mpv = mapCloud(pos);
		float den = clamp(mpv.x-0.3,0.,1.)*1.12;
		float dn = clamp((mpv.x + 2.),0.,3.);

		vec4 col = vec4(0);
        if (mpv.x > 0.6)
        {

            col = vec4(sin(vec3(5.,0.4,0.2) + mpv.y*0.1 +sin(pos.z*0.4)*0.5 + 1.8)*0.5 + 0.5,0.08);
            col *= den*den*den;
			col.rgb *= linstep(4.,-2.5, mpv.x)*2.3;
            float dif =  clamp((den - mapCloud(pos+.8).x)/9., 0.001, 1. );
            dif += clamp((den - mapCloud(pos+.35).x)/2.5, 0.001, 1. );
            col.xyz *= den*(vec3(0.005,.045,.075) + 1.5*vec3(0.033,0.07,0.03)*dif);
        }

		float fogC = exp(t*0.2 - 2.2);
		col.rgba += vec4(0.06,0.11,0.11, 0.1)*clamp(fogC-fogT, 0., 1.);
		fogT = fogC;
		rez = rez + col*(1. - rez.a);
		t += clamp(0.5 - dn*dn*.05, 0.09, 0.3);
	}
	return clamp(rez, 0.0, 1.0);
}


// sky
vec3 getSkyColor(vec3 e) {
    e.y = (max(e.y,0.0)*0.8+0.2)*0.8;
    vec3 color = vec3(pow(1.0-e.y,2.0), 1.0-e.y, 0.6+(1.0-e.y)*0.4) * 1.1;
    //get coords and direction
	vec2 uv=gl_FragCoord.xy/iResolution.xy-.5;
	uv.y*=iResolution.y/iResolution.y;
	vec3 dir=vec3(uv,1.);
	float time=iTime*speed+.25;
    float s=0.1,fade=1.;
	vec3 v=vec3(0.);
	for (int r=0; r<volsteps; r++) {
		vec3 p=s*dir*.5;
		p = abs(vec3(tile)-mod(p,vec3(tile*2.))); // tiling fold
		float pa,a=pa=0.;
		for (int i=0; i<iterations; i++) {
			p=abs(p)/dot(p,p)-formuparam; // the magic formula
			a+=abs(length(p)-pa); // absolute sum of average change
			pa=length(p);
		}
		float dm=max(0.,darkmatter-a*a*.001); //dark matter
		a*=a*a; // add contrast
		if (r>6) fade*=1.-dm; // dark matter, don't render near
		//v+=vec3(dm,dm*.5,0.);
		v+=fade;
		v+=vec3(s,s*s,s*s*s*s)*a*brightness*fade; // coloring based on distance
		fade*=distfading; // distance fading
		s+=stepsize;
	}
	v=mix(vec3(length(v)),v,saturation); //color adjust
    return color * v * 0.01;
}

// sea
float sea_octave(vec2 uv, float choppy) {
    uv += noise(uv);
    vec2 wv = 1.0-abs(sin(uv));
    vec2 swv = abs(cos(uv));
    wv = mix(wv,swv,wv);
    return pow(1.0-pow(wv.x * wv.y,0.65),choppy);
}

//sand islands
float island_octave(vec2 uv, float choppy) {
    uv += noise(uv);
    vec2 wv = 1.0-abs(sin(uv));
    vec2 swv = abs(cos(uv));
    wv = mix(wv,swv,wv);
    return pow(1.0-pow(wv.x * wv.y,0.65),choppy);
}

vec3 getSandColor(vec3 p) {
    float noise1 = island_octave(p.xz * 0.2 + 0.1, 0.5) * 0.7;
    float noise2 = island_octave(p.xz * 1.0 + 0.5, 0.3) * 0.3;
    return SAND_COLOR * (noise1 + noise2);
}

float map(vec3 p) {
    float freq = SEA_FREQ;
    float amp = SEA_HEIGHT;
    float choppy = SEA_CHOPPY;
    vec2 uv = p.xz; uv.x *= 0.75;

    float d, h = 0.0;
    for(int i = 0; i < ITER_GEOMETRY; i++) {
        d = sea_octave((uv+SEA_TIME)*freq,choppy);
        d += sea_octave((uv-SEA_TIME)*freq,choppy);
        h += d * amp;
    	uv *= octave_m; freq *= 1.9; amp *= 0.22;
        choppy = mix(choppy,1.0,0.2);
    }
    return p.y - h;
}

float map_detailed(vec3 p) {
    float freq = SEA_FREQ;
    float amp = SEA_HEIGHT;
    float choppy = SEA_CHOPPY;
    vec2 uv = p.xz; uv.x *= 0.75;

    float d, h = 0.0;
    for(int i = 0; i < ITER_FRAGMENT; i++) {
        d = sea_octave((uv+SEA_TIME)*freq,choppy);
        d += sea_octave((uv-SEA_TIME)*freq,choppy);
        h += d * amp;
    	uv *= octave_m; freq *= 1.9; amp *= 0.22;
        choppy = mix(choppy,1.0,0.2);
    }
    return p.y - h;
}

vec3 getSeaColor(vec3 p, vec3 n, vec3 l, vec3 eye, vec3 dist) {
    float fresnel = clamp(1.0 - dot(n,-eye), 0.0, 1.0);
    fresnel = pow(fresnel, 20.);
    fresnel = min(pow(fresnel,3.0), 0.5);

    vec3 reflected = getSkyColor(reflect(eye,n));
    vec3 refracted = SEA_BASE + diffuse(n,l,80.0) * SEA_WATER_COLOR * 0.12;

    vec3 color = mix(refracted,reflected,fresnel);

    float atten = max(1.0 - dot(dist,dist) * 0.001, 0.0);
    color += SEA_WATER_COLOR * (p.y - SEA_HEIGHT) * 0.18 * atten;

    color = mix(color, vec3(specular(n,l,eye,60.0)), pow(smoothstep(0.0, -0.02, l.y), 0.2));

    vec2 st = gl_FragCoord.xy / iResolution.xy * 3.0;
    st += st * abs(sin(iTime * 0.01) * 2.0);

    vec2 q = vec2(0.0);
    q.x = fbm(st + vec2(0.0, 0.0) * 10.0);
    q.y = fbm(st + vec2(1.0, 0.0));

    vec2 r = vec2(0.0);
    r.x = fbm(st + (q * 1.0) + vec2(1.7, 9.2) + (0.15 * 10.0));
    r.y = fbm(st + (q * 1.0) + vec2(8.3, 2.8) + (0.126 * 10.0));

    float f = fbm(st + r);

    vec3 color2 = mix(color,
        vec3(0.0, 0.0, 0.164706),
        clamp(length(q), 0.0, 1.0));

    vec3 color3 = mix(color2,
        vec3(0.666667, 1.0, 1.0),
        clamp(length(r.x), 0.0, 1.0));

    color = mix(color3, color, 0.75);

    return color;
}

// tracing
vec3 getNormal(vec3 p, float eps) {
    vec3 n;
    n.y = map_detailed(p);
    n.x = map_detailed(vec3(p.x+eps,p.y,p.z)) - n.y;
    n.z = map_detailed(vec3(p.x,p.y,p.z+eps)) - n.y;
    n.y = eps;
    return normalize(n);
}

float heightMapTracing(vec3 ori, vec3 dir, out vec3 p) {
    float tm = 0.0;
    float tx = 1000.0;
    float hx = map(ori + dir * tx);
    if(hx > 0.0) {
        p = ori + dir * tx;
        return tx;
    }
    float hm = map(ori + dir * tm);
    float tmid = 0.0;
    for(int i = 0; i < NUM_STEPS; i++) {
        tmid = mix(tm,tx, hm/(hm-hx));
        p = ori + dir * tmid;
        float hmid = map(p);
		if(hmid < 0.0) {
            tx = tmid;
            hx = hmid;
        } else {
            tm = tmid;
            hm = hmid;
        }
    }
    return tmid;
}

vec3 calculateSphereColor(vec3 spherePos, vec3 sphereNormal, vec3 light, float time) {
    vec2 q = gl_FragCoord.xy/iResolution.xy;
    vec2 p = (gl_FragCoord.xy - 0.5*iResolution.xy)/iResolution.y;
    bsMo = (iMouse.xy - 0.5*iResolution.xy)/iResolution.y;

    time = iTime*3.;
    vec3 ro = vec3(0,0,time);

    ro += vec3(sin(iTime)*0.5,sin(iTime*1.)*0.,0);

    float dspAmp = .85;
    ro.xy += disp(ro.z)*dspAmp;
    float tgtDst = 3.5;

    vec3 target = normalize(ro - vec3(disp(time + tgtDst)*dspAmp, time + tgtDst));
    ro.x -= bsMo.x*2.;
    vec3 rightdir = normalize(cross(target, vec3(0,1,0)));
    vec3 updir = normalize(cross(rightdir, target));
    rightdir = normalize(cross(updir, target));
	vec3 rd=normalize((p.x*rightdir + p.y*updir)*1. - target);
    rd.xy *= rot(-disp(time + 3.5).x*0.2 + bsMo.x);
    prm1 = smoothstep(-0.4, 0.4,sin(iTime*0.3));
	vec4 scn = renderCloud(ro, rd, time);

    vec3 col = scn.rgb;
    col = iLerp(col.bgr, col.rgb, clamp(1.-prm1,0.05,1.));

    col = pow(col, vec3(.55,0.65,0.6))*vec3(1.,.97,.9);

    col *= pow( 16.0*q.x*q.y*(1.0-q.x)*(1.0-q.y), 0.12)*0.7+0.3; //Vign

    return col;
}


vec3 renderSea(vec3 ori, vec3 dir, vec3 light) {
    vec3 p;
    heightMapTracing(ori, dir, p);
    vec3 dist = p - ori;
    vec3 n = getNormal(p, dot(dist, dist) * EPSILON_NRM);
    return mix(getSkyColor(dir), getSeaColor(p, n, light, dir, dist), pow(smoothstep(0.0, -0.02, dir.y), 0.2));
}

vec3 getPixel(in vec2 coord, float time) {
    vec2 uv = coord / iResolution.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= iResolution.x / iResolution.y;

    // Camera setup
    float u_cameraPositionZ = (sin(iTime * 0.1) + 1.0) * 0.5 * 1.0 + 1.0;
    uv /= u_cameraPositionZ;

    // Ray setup
    vec3 ang = vec3(sin(time * 3.0) * 0.01, sin(time) * 0.01 + 0.2, 0.4);
    vec3 ori = vec3(0.0, 3.5, 20.0);
    vec3 dir = normalize(vec3(uv.xy, -2.0));
    dir.z += length(uv) * 0.14;
    dir = normalize(dir) * fromEuler(ang);

    // Lighting
    vec3 light = normalize(vec3(0.0, 1.0, 0.8));

    // Initialize variables for color and hit detection
    vec3 color = vec3(0.0);
    bool hitSomething = false;

    // Check intersection with each sphere
    for (int i = 0; i < 3; i++) {
        float waterLevelAtSphere = map(vec3(sphereCenters[i].x, 0.0, sphereCenters[i].z));
        vec3 adjustedSphereCenter = sphereCenters[i];
        adjustedSphereCenter.y = max(waterLevelAtSphere, sphereCenters[i].y);
        float tSphere = raySphereIntersect(ori, dir, adjustedSphereCenter, sphereRadii[i]);
        if (tSphere > 0.0) {
            hitSomething = true;
            vec3 spherePos = ori + dir * tSphere;
            vec3 sphereNormal = normalize(spherePos - sphereCenters[i]);

            vec3 p;
            heightMapTracing(ori, dir, p);
            vec3 dist = p - ori;
            vec3 n = getNormal(p, dot(dist, dist) * EPSILON_NRM);
            sphereNormal = mix(sphereNormal, n, 0.075);
            float blendFactor = smoothstep(waterLevelAtSphere - 0.6, waterLevelAtSphere + 0.3, spherePos.y);

            // Compute color for the sphere
            vec3 sphereColor = calculateSphereColor(spherePos, sphereNormal, light, time + spherePos.x);

            vec3 seaColor = getSeaColor(p, n, light, dir, dist);
            color = mix(seaColor, sphereColor, blendFactor);
        }
    }

    // Render sea if no sphere was hit
    if (!hitSomething) {
        color = renderSea(ori, dir, light);
    }

    return color;
}

// main
void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
    float time = iTime * 0.1;
#ifdef AA
    vec3 color = vec3(0.0);
    for(int i = -1; i <= 1; i++) {
        for(int j = -1; j <= 1; j++) {
            vec2 uv = (fragCoord + vec2(i, j) / 3.0);
            color += getPixel(uv, time);
        }
    }
    color /= 9.0;
#else
    vec3 color = getPixel(fragCoord, time);
#endif

    // post
	fragColor = vec4(pow(color,vec3(0.65)), 1.0);
}
