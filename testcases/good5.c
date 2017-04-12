#include<stdio.h>
struct s {
    int a;
};

int * f(void * a) {
    return a;
}

void main() {
    struct s a, *p;
    int * ip;
    a.a = 3;
    p = &a;
    ip = f(p);
    printf("%d",*ip);
}
