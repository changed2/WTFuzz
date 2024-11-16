#include <stdio.h>
#include <string.h>

#define BUFFER_SIZE 512
#define INPUT_SIZE 1024

int main() {
    char data[INPUT_SIZE]; 

    printf("Enter the XML data:\n");
    fgets(data, INPUT_SIZE, stdin);

    char *start = strstr(data, "<test_key>");
    char *end = strstr(data, "</test_key>");
    if (!start || !end) {
        printf("Error: <test_key> not found in the input.\n");
        return 1;
    }

    char buffer[BUFFER_SIZE];

    strcpy(buffer, start);

    printf(buffer);

    return 0;
}