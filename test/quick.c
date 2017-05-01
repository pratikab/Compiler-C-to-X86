#include<stdio.h>
int arr[10]; 
int quick_sort(int low,int high)
{
 int pivot,j,temp,i;
 if(low<high)
 {
  pivot = low;
  i = low;
  j = high;
 
  while(i<j)
  {
while((arr[i]<=arr[pivot])&&(i<high))
   {
    i++;
   }
   while(arr[j]>arr[pivot])
   {
    j--;
   }
   if(i<j)
   { 
	temp=arr[i];
    int temp2 = arr[j];
	arr[i]=temp2;
    
	arr[j]=temp;
   }

  }
printInt(pivot);printInt(j);
  temp=arr[pivot];
  arr[pivot]=arr[j];
  arr[j]=temp;
  int t  = j-1;
  int q = j+1;
  quick_sort(low,t);
  quick_sort(q,high);
 return 0;
 }
} 
 
int main()
{
int  n = 4,i;
 
 	arr[0] = 1;
 	arr[1] = 2;
	arr[2] = 4;
	arr[3] = 3;
int p = n-1;
 quick_sort(1,p);
for(i = 1;i<n;i++){
//printf("%d",arr[i]);
printInt(arr[i]);
}
return 0;
}
 

