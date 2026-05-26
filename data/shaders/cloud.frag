#version 330

in vec2 uvs;

uniform sampler2D tex;
uniform float uTime;

out vec4 FragColor;


vec3 DAY_COLOR   = vec3(243, 237, 249);
vec3 NIGHT_COLOR = vec3(181, 160, 203);


float remap(float value, float min1, float max1, float min2, float max2) {
    return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}


void main() {

    vec4 textureColor = texture(tex, uvs);

    float t = mod(uTime, 2400.0);

    vec3 lightColor = DAY_COLOR;

    if (t < 600.0) {
        lightColor = NIGHT_COLOR;
    }
    else if (t < 900.0) {
        float f = remap(t, 600.0, 900.0, 0.0, 1.0);
        lightColor = mix(NIGHT_COLOR, DAY_COLOR, f);
    }
    else if (t < 1800.0) {
        lightColor = DAY_COLOR;
    }
    else if (t < 2000.0) {
        float f = remap(t, 1800.0, 2000.0, 0.0, 1.0);
        lightColor = mix(DAY_COLOR, NIGHT_COLOR, f);
    }
    else { lightColor = NIGHT_COLOR; }
    lightColor += uvs.x * 0.1;

    FragColor = vec4((textureColor.rgb * lightColor) / 255.0, textureColor.a);
}