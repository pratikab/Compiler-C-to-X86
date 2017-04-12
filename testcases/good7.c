#include<stdio.h>
int printf();
int f (int b ) {
    int a;
    a=5;
    return a;
}

int main () {
    int a,b;
    a = 9;
    b = f(a);
    printf("%d\n%d",a,b);
}
