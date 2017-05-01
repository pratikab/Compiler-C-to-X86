int ARRAY[10];
int left_child(int a){
	int p = (2 *a) + 1;
	return p;
}
int right_child(int a){
	int p = (2*a)+2;
	return p;
}
int in_order(int head){
	if(head>=7){
	 return 0;
	}
	int left = left_child(head);
	int right = right_child(head);
	in_order(left);
	int k = head;
	printInt(ARRAY[k]);
	in_order(right);
	return 0;
	
}
int main(){
	ARRAY[0] = 5;
	ARRAY[1] = 3;
	ARRAY[2] = 6;
	ARRAY[3] = 1;
	ARRAY[4] = 2;
	ARRAY[5] = 4;
	ARRAY[6] = 7;
	int head = 0;
	in_order(head);
	return 0;
	
}
