#include <stdio.h>
#include <string.h>

int main() {

    printf("=== BUFFER OVERFLOW DEMO ===\n\n");

    struct {
        char buffer[8];
        int flag;
    } data;

    data.flag = 12345;

    printf("Initial flag value: %d\nThe flag value should not change \n", data.flag);

    printf("\n[Unsafe] Enter more than 7 characters: ");
    scanf("%s", data.buffer);  // No bounds check

    printf("Buffer content: %s\n", data.buffer);
    printf("Flag value after unsafe input: %d  ----> Memory corruption \n", data.flag);

    printf("\n[Safe Version]\n");

    struct {
        char buffer[8];
        int flag;
    } safe_data;

    safe_data.flag = 12345;

    printf("Initial flag value: %d\n", safe_data.flag);

    printf("Enter up to 7 characters safely: ");
    scanf("%7s", safe_data.buffer);  // Bounds check

    printf("Buffer content: %s\n", safe_data.buffer);
    printf("Flag value after safe input: %d\n", safe_data.flag);

    return 0;
}