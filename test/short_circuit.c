int main(){
	int a = 2;int b = 4;
	if(a == 2 && b == 4){
		printInt(1);
	}
	if(a == 3 && b == 4){
		printInt(2);
	}

        if(a == 1 ||  b ==3){
                printInt(3);
        }
	if(a == 2 ||  b == 4){
                printInt(4);
        }
	return 0;

}
