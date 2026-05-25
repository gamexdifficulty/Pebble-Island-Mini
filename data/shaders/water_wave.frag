#version 330

in vec2 uvs;
out vec4 FragColor;

uniform float uTime;

float waterLevel = 0.2;
float amplitude = 0.0625;

vec3 waterColor_Top    = vec3(77.0/255.0, 101.0/255.0, 180.0/255.0);
vec3 waterColor_Middle = vec3(84.0/255.0, 128.0/255.0, 206.0/255.0);

void main() {

    float y = 1.0 - uvs.y;

    if (y > waterLevel) {
        FragColor = vec4(0.0, 0.0, 0.0, 0.0);
        return;
    }

    float uTime = uTime/3;

    float localY = y / waterLevel;

    float wave_up_down_1 = sin(uTime) * 0.4;
    float wave1_1 = sin(uvs.x * 20.0 + (uTime) * 2.0);
    float wave1_2 = cos(uvs.x * 40.0 + (uTime) * 0.5);
    float combined_1 = (wave_up_down_1 * 2.0 + wave1_1 + wave1_2);
    float waveY_1 = 0.85 + combined_1 * amplitude;

    float wave_up_down_2 = sin(uTime) * 0.4;
    float wave2_1 = sin(uvs.x * 20.0 + ((uTime) + 10.0) * 2.0);
    float wave2_2 = cos(uvs.x * 40.0 + ((uTime) + 10.0) * 0.5);
    float combined_2 = (wave_up_down_2 * 2.0 + wave2_1 + wave2_2);
    float waveY_2 = 0.45 + combined_2 * amplitude;

    if (localY > waveY_1) { FragColor = vec4(0.0, 0.0, 0.0, 0.0); }
    else if (localY > waveY_2) { FragColor = vec4(waterColor_Top, 1.0); }
    else { FragColor = vec4(waterColor_Middle, 1.0); }
}