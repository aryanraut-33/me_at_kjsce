#include <stdio.h>

int main() {

    printf("[NULL TERMINATION DEMO]\n\n");

    printf("[UNSAFE VERSION]\n");

    char str1[5] = {'H','e','l','l','o'};  // No '\0'

    printf("Memory layout (conceptual):\n");
    printf("str1: H e l l o  (NO NULL TERMINATOR)\n");
    printf("extra: X Y Z \\0\n\n");

    printf("Printing str1 using %%s:\n");
    printf("%s\n", str1);

    printf("\nExplanation:\n");
    printf("Since str1 has NO '\\0', printf keeps reading memory\n");
    printf("until it accidentally finds a '\\0'.\n");
    printf("It may print extra characters from adjacent memory.\n\n");


    printf("[SAFE VERSION]\n");

    char str2[6] = "Hello";  // Automatically adds '\0'

    printf("Memory layout (conceptual):\n");
    printf("str2: H e l l o \\0\n\n");

    printf("Printing str2 using %%s:\n");
    printf("%s\n", str2);

    printf("\nExplanation:\n");
    printf("str2 ends with '\\0'.\n");
    printf("printf stops exactly at the null terminator.\n");
    printf("No extra memory is read.\n");

    return 0;
}