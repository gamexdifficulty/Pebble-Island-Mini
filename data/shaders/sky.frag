#version 330

in vec2 uvs;

uniform float uTime;

out vec4 FragColor;

vec3 NIGHT = vec3(32, 35, 52);
vec3 DAY   = vec3(76, 139, 216);

vec3 SUNRISE_1 = vec3(86, 61, 162);
vec3 SUNRISE_2 = vec3(225, 155, 95);

vec3 SUNSET_1  = vec3(145, 95, 185);

float remap(float value, float min1, float max1, float min2, float max2) {
    return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

void main() {

    float t = mod(uTime, 2400.0);

    vec3 color = NIGHT;

    if (t < 600.0) {
        color = NIGHT;
    }
    else if (t < 720.0) {
        float f = remap(t, 600.0, 720.0, 0.0, 1.0);
        color = mix(NIGHT, SUNRISE_1, f);
    }
    else if (t < 820.0) {
        float f = remap(t, 720.0, 820.0, 0.0, 1.0);
        color = mix(SUNRISE_1, SUNRISE_2, f);
    }
    else if (t < 900.0) {
        float f = remap(t, 820.0, 900.0, 0.0, 1.0);
        color = mix(SUNRISE_2, DAY, f);
    }
    else if (t < 1800.0) {
        color = DAY;
    }
    else if (t < 1900.0) {
        float f = remap(t, 1800.0, 1900.0, 0.0, 1.0);
        color = mix(DAY, SUNSET_1, f);
    }
    else if (t < 2000.0) {
        float f = remap(t, 1900.0, 2000.0, 0.0, 1.0);
        color = mix(SUNSET_1, NIGHT, f);
    }
    else { color = NIGHT;}

    color += uvs.x * 0.1;
    FragColor = vec4(color / 255.0, 1.0);
}