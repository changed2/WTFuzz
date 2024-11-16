#include <stdio.h>
#include <string.h>

#define BUFFER_SIZE 32

int main(int argc, char *argv[]) {
    FILE *file = fopen(argv[1], "r");
    char data[512];
    fread(data, 1, sizeof(data), file);
    fclose(file);

    char buffer[BUFFER_SIZE];
    char *start = strstr(data, "\"test_key\":");
    strcpy(buffer, start + 11);
    printf("%s\n", buffer);
    return 0;
}