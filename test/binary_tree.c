int b[10];
int left_child(int a){
	int p = (2 *a) + 1;
	return p;
}
int right_child(int a){
	int p = (2*a)+2;
	return p;
}
int in_order(int head){
//	printInt(b[5]);
	if(head>=7){
	 return 0;
	}
	int left = left_child(head);
	int right = right_child(head);
	in_order(left);
	int k = head;
	printInt(k);
	in_order(right);
	return 0;
	
}
int main(){
	b[0] = 5;
	b[1] = 3;
	b[2] = 6;
	b[3] = 1;
	b[4] = 2;
	b[5] = 4;
	b[6] = 7;
	int head = 0;
	in_order(head);
	return 0;
	
}
