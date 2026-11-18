#include <stdio.h>

void vulnerable() {
    char buffer[8];
    int check = 999;

    printf("\nInside vulnerable function\n");
    printf("Initial check value: %d\n", check);

    printf("Enter more than 7 characters: ");
    scanf("%s", buffer);  // Unsafe

    printf("Check value after input: %d\n", check);
}

void safe() {
    char buffer[8];
    int check = 999;

    printf("\nInside safe function\n");
    printf("Initial check value: %d\n", check);

    printf("Enter up to 7 characters safely: ");
    scanf("%7s", buffer);

    printf("Check value after input: %d\n", check);
}

int main() {

    printf("=== STACK SMASHING DEMO ===\n");

    printf("\n[Unsafe Version]");
    vulnerable();

    printf("\n[Safe Version]");
    safe();

    return 0;
}