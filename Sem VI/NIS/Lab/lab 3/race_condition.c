#include <stdio.h>
#include <pthread.h>

int counter = 0;
pthread_mutex_t lock;


void* increment_unsafe(void* arg) {
    for(int i = 0; i < 100000; i++) {
        counter++;   // Not atomic (Read → Modify → Write)
    }
    return NULL;
}


void* increment_safe(void* arg) {
    for(int i = 0; i < 100000; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main() {

    printf("[RACE CONDITION DEMO]\n\n");

    pthread_t t1, t2;


    printf("[UNSAFE VERSION]\n");
    printf("Two threads increment counter 100000 times each.\n");
    printf("Expected final value = 200000\n\n");

    counter = 0;

    pthread_create(&t1, NULL, increment_unsafe, NULL);
    pthread_create(&t2, NULL, increment_unsafe, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Actual final value   = %d\n\n", counter);

    printf("Explanation:\n");
    printf("counter++ is NOT atomic.\n");
    printf("It performs: Read → Add → Write.\n");
    printf("If two threads read the same value before writing,\n");
    printf("one update gets lost. This is called a LOST UPDATE.\n\n");

    printf("[SAFE VERSION USING MUTEX]\n");

    counter = 0;
    pthread_mutex_init(&lock, NULL);

    pthread_create(&t1, NULL, increment_safe, NULL);
    pthread_create(&t2, NULL, increment_safe, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Expected final value = 200000\n");
    printf("Actual final value   = %d\n\n", counter);

    printf("Explanation:\n");
    printf("Mutex ensures only one thread updates counter at a time.\n");
    printf("No lost updates occur.\n");

    pthread_mutex_destroy(&lock);

    return 0;
}