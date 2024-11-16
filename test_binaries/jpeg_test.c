#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 256

void process_jpeg(const char *filename) {
    FILE *file = fopen(filename, "rb");

    unsigned char buffer[BUFFER_SIZE];
    fread(buffer, 1, BUFFER_SIZE, file);
    unsigned char *dynamicBuffer = (unsigned char *)malloc(BUFFER_SIZE);
    memcpy(dynamicBuffer, buffer, BUFFER_SIZE);

    for (size_t i = 0; i < BUFFER_SIZE; i++) {
        if (dynamicBuffer[i] == 0xFF) {
            printf("Found marker at position %zu\n", i);
        }
    }
    free(dynamicBuffer);
    fclose(file);
}

int main(int argc, char *argv[]) {
    process_jpeg(argv[1]);
    return 0;
}