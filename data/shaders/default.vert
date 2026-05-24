#version 330
uniform vec2 offset;
uniform vec2 scale_pixels;
uniform vec2 screen_size;
uniform float rotation;
uniform float alpha;
uniform vec2 pivot;
uniform bool flipped;

in vec2 vert;
in vec2 tex;
out vec2 uvs;

void main() {
    float c = cos(rotation);
    float s = sin(rotation);

    vec2 local = vert - pivot;
    vec2 scaled = local * scale_pixels;
    vec2 rotated = vec2(
        scaled.x * c - scaled.y * s,
        scaled.x * s + scaled.y * c
    );

    vec2 transformed = rotated + pivot * scale_pixels;
    vec2 ndc = vec2(
        transformed.x * 2.0 / screen_size.x,
        transformed.y * 2.0 / screen_size.y
    );

    gl_Position = vec4(offset + ndc, 0.0, 1.0);
    
    if (flipped) {
        uvs = vec2(1.0 - tex.x, tex.y);
    } else {
        uvs = tex;
    }
}