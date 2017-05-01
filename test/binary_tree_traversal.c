#include <iostream>
using namespace std;
int leftchild(int nodeindex) // returns the index of the left child
{
    return  nodeindex *2 + 1 ;
}
int rightchild(int nodeindex) // returns the index of the right child
{
    return nodeindex * 2 +2;
}
// changed i to a reference because left children must be able to increment it before node writes its own data
int inorder(int* mas, int nodeindex, int& i) // a recursive function to print the nodes values, put in array
{
	if (mas[nodeindex] == 0) return 0 ;
	inorder(mas, leftchild(nodeindex), i) ;
	cout << mas[nodeindex] << ' ';
	inorder(mas,  rightchild(nodeindex), ++i); // pre-incrementing the array index i for the right child
}
int main () {
    int mas[93]={2,3,1,9,8,7,6,5};  // only 8 non-zero elements
    int i = 0,j; // added index variable to pass to recursive function
    inorder(mas, 0, i);
    for (i=0;i<8;i++){
    	for(j=0;j<8;j++){
			if(mas[j] == 0){
				break;
			}
    	}
    }
    return 0;
}