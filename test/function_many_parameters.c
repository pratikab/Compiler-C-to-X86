int func(int a,int b, int c, int d, int e, int f, int g, int h, int i){
	int sum = a + b + c+ d +e + f +g +h +i;
	return sum;
}

int main(){
	int a;
	a = func(1,2,3,4,5,6,7,8,9);
	printInt(a);
	return 0;
}