#include<stdio.h>
int printf();

void main()
{
    int x;
    int y;
    float a;
    float b;
    int i;
    int j;
    x = 10;
    y = -1;
    for(i=0; i<10; i++){
        y = -y;
        x = x + i*y;
        i = - (-i);
    }

    a = 10.0;
    b = -0.1;
    for(i=0; i<10;i++){
        b=-b;
        a  = a+i*b;
        i= - (-i);
    }

    printf("Expected output:5 9.500000\n");

    printf("%d", x);

    printf("%f", a);
    printf("\n");
}
