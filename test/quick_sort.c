#include <stdio.h>
#include <stdbool.h>
// #define MAX 7

// int intArray[MAX] = {4,6,3,2,1,9,7};

// void printline(int count) {
//    int i;
      
//    for(i = 0;i <count-1;i++) {
//       printf("=");
//    }
      
//    printf("=\n");
// }

// void display() {
//    int i;
//    printf("[");
//    for(i = 0;i<MAX;i++) {
//       printf("%d ",intArray[i]);
//    }
      
//    printf("]\n");
// }

int intArray[7];

int swap(int num1, int num2) {
   int temp = intArray[num1];
   intArray[num1] = intArray[num2];
   intArray[num2] = temp;
}

int partition(int left, int right, int pivot) {
   int leftPointer = left -1;
   int rightPointer = right;
   int a = 1;
   while(a ==1) {
      while(intArray[leftPointer] < pivot) {
         leftPointer = leftPointer + 1;
      }
            
      while(rightPointer > 0 && intArray[rightPointer] > pivot) {
         rightPointer = rightPointer -1;
      }

      if(leftPointer >= rightPointer) {
         break;
      } else {
         swap(leftPointer,rightPointer);
      }
   }
      
   swap(leftPointer,right);
   return leftPointer;
}

int quickSort(int left, int right) {
   if(right-left <= 0) {
      return;   
   } else {
      int pivot = intArray[right];
      int partitionPoint = partition(left, right, pivot);
      quickSort(left,partitionPoint-1);
      quickSort(partitionPoint+1,right);
   }        
}

int main() {
   int MAX = 7;
   intArray[0] = 4;
   intArray[1] = 6;
   intArray[2] = 3;
   intArray[3] = 2;
   intArray[4] = 1;
   intArray[5] = 9;
   intArray[6] = 7;
   quickSort(0,MAX-1);
   printInt(intArray[0]);
}