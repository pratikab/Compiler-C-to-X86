int* returnPointerToInt () {
    int* a;
    return a;
}


int main () {
    int a;
    int b;
    int c[3];


    c[returnPointerToInt()] = 2;
}
