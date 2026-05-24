#version 330

uniform sampler2D tex0;
in vec2 v_uv;
out vec4 fragColor;

void main() {
    fragColor = texture(tex0, v_uv);
}
