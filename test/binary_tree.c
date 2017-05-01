int left_child(int a){
	int p = (2 *a) + 1;
	return p;
}
int right_child(int a){
	int p = (2*a)+2;
	return p;
}

int main(){
	int a[7];
	a[0] = 5;
	a[1] = 3;
	a[2] = 6;
	a[3] = 1;
	a[4] = 2;
	a[5] = 4;
	a[6] = 7;
	int head = 6;
	int i;
	for(i = 0;i<7;i++){
		if(a[i] == head){
			break;
		}
	}
	
	int l = left_child(i);
	printInt(a[l]);
	int r = right_child(i);
	printInt(a[r]);
	return 0;
	
}
