/*
 * This program dumps information about a WebP File on to
 * the console.
 *
 * WebP Format Spec: https://developers.google.com/speed/webp/docs/riff_container
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>

// reads a 32 bit little endian integer
#define RL32(x) \
    (((uint32_t)((const uint8_t*)(x))[3] << 24) | \
    (((const uint8_t*)(x))[2] << 16) | \
    (((const uint8_t*)(x))[1] <<  8) | \
    ((const uint8_t*)(x))[0])

// reads a 24 bit little endian integer
#define RL24(x) \
    ((((const uint8_t*)(x))[2] << 16) | \
    (((const uint8_t*)(x))[1] <<  8) | \
    ((const uint8_t*)(x))[0])

#define RL16(x) \
    ((((const uint8_t*)(x))[1] << 8) | \
    ((const uint8_t*)(x))[0])

void indent(int level) {
    int i = 0;
    for (; i < level; i++) {
        fprintf(stdout, "    ");
    }
}

void print(const char *const str, uint32_t size, int indent_level) {
    indent(indent_level);
    fprintf(stdout, "+ %s (size: %u)\n", str, size);
}

int get_nth_bit(uint8_t byte, int n) {
    return byte & (1 << (8 - n));
}

void parse_vp8x(FILE *fp, uint32_t size, int level) {
    uint32_t consumed = 0;

    //read and parse the flags
    uint8_t flags;
    int should_indent = 1;
    char bits[5][20] = {"ICC Profile", "Alpha", "EXIF Metadata",
                        "XMP Metadata", "Animation"};
    int i;
    fread(&flags, 1, 1, fp);
    consumed++;
    for (i = 3; i <= 7; i++) {
        if (get_nth_bit(flags, i)) {
            if (should_indent) {
                indent(level);
                fprintf(stdout, "Flags: ");
                should_indent = 0;
            }
            fprintf(stdout, "%s; ", bits[i - 3]);
        }
    }
    if (!should_indent) fprintf(stdout, "\n");

    // read and parse the canvas size
    uint8_t data[6];
    fseek(fp, 3, SEEK_CUR); // skip reserve bits
    fread(data, 1, 6, fp);
    consumed += 9;
    uint32_t width = RL24(data) + 1;
    indent(level);
    fprintf(stdout, "Canvas Width: %u\n", width);
    uint32_t height = RL24(&data[3]) + 1;
    indent(level);
    fprintf(stdout, "Canvas Height: %u\n", height);

    // set the file pointer to the end of the chunk
    fseek(fp, size - consumed, SEEK_CUR);
}

void parse_anim(FILE *fp, uint32_t size, int level) {
    int consumed = 0;

    // read and parse the background color and loop count
    uint8_t colors_and_count[6];
    fread(colors_and_count, 1, 6, fp);
    consumed += 6;
    indent(level);
    fprintf(stdout, "Background Color: BGRA (");
    int i;
    for (i = 0; i < 4; i++) {
        fprintf(stdout, "%u", colors_and_count[i]);
        if (i != 3) fprintf(stdout, ", ");
    }
    fprintf(stdout, ")\n");
    uint16_t loop_count = RL16(&colors_and_count[4]);
    indent(level);
    fprintf(stdout, "Loop Count: %u", loop_count);
    if (!loop_count) fprintf(stdout, " (infinite)");
    fprintf(stdout, "\n");

    // set the file pointer to the end of the chunk
    fseek(fp, size - consumed, SEEK_CUR);
}

int read_riff(const char *filename) {
    // constants
    const char *const kRiffHeader = "RIFF";
    const char *const kWebPHeader = "WEBP";

    // input file
    FILE *fp = fopen(filename, "rb");

    // indent level
    int level = 0;

    // start by reading the riff header
    char riff_header[8] = {0};
    if (8 != fread(riff_header, 1, 8, fp) ||
        strncmp(riff_header, kRiffHeader, 4)) {
        fprintf(stderr, "Not a RIFF file\n");
        return 1;
    }
    uint32_t riff_size = RL32(&riff_header[4]);
    print(kRiffHeader, riff_size, level++);
    if (!riff_size) {
        fprintf(stderr, "Not a WebP file\n");
        return 1;
    }

    // read the WEBP 4cc.
    char webp_header[4] = {0};
    if (4 != fread(webp_header, 1, 4, fp) ||
        strncmp(webp_header, kWebPHeader, 4)) {
        fprintf(stderr, "Not a WebP file\n");
        return 1;
    }

    // read the chunks
    do {
        char data[8];
        if (8 != fread(data, 1, 8, fp)) break;
        char chunk_header[5] = {0};
        memcpy(chunk_header, data, 4);
        uint32_t chunk_size = RL32(&data[4]);
        print(chunk_header, chunk_size, level);
        if (!strncmp(chunk_header, "VP8X", 4)) {
            parse_vp8x(fp, chunk_size, level + 1);
        } else if (!strncmp(chunk_header, "ANIM", 4)) {
            parse_anim(fp, chunk_size, level + 1);
        } else {
            fseek(fp, chunk_size, SEEK_CUR);
        }
    } while (!feof(fp));
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 0;
    }
    return read_riff(argv[1]);
}