#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <json-c/json.h>

int main() {
    char buffer[1024];

    fgets(buffer, sizeof(buffer), stdin);

    struct json_object *parsed_json;
    struct json_object *message;

    parsed_json = json_tokener_parse(buffer);
    json_object_object_get_ex(parsed_json, "message", &message);

    printf(json_object_get_string(message));

    return 0;
}