#version 330
uniform sampler2D Texture;
uniform float alpha;
in vec2 uvs;
out vec4 fragColor;

void main() {
    vec4 texColor = texture(Texture, uvs);
    fragColor = vec4(texColor.rgb, texColor.a * alpha);
}