#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char* getField(char* line, int num)
{
    char* tok = strtok(line, ",");
    if (!--num) {
            return tok;
    }
    while ((tok = strtok(NULL, ",")) != NULL) {
        if (!--num) {
            return tok;
        }
    }
    return NULL;
}

int main()
{
    char line[1024];
    fgets(line, 1024, stdin);
    for(int i = 0; i < 3; i++) {
        fgets(line, 1024, stdin);
        char* tmp = strdup(line);
        printf("%d\n", atoi(getField(tmp, atoi(getField(tmp, 1)))));
        free(tmp);
    }
}