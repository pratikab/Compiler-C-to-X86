int main()
{
   int c, first, last, middle, n, search;
   n = 10;
int array[10];
 array[0] = 0;
 array[1] = 2;
 array[2] = 3;
 array[3] = 4;
 array[4] = 8;
 array[5] = 89;
 array[6] = 435;
 array[7] = 545;
 array[8] = 654;
 array[9] = 854;
    
    printInt(array[0]);
    printInt(array[1]);
    printInt(array[2]);
    printInt(array[3]);
    printInt(array[4]);
    printInt(array[5]);
    printInt(array[6]);
    printInt(array[7]);
    printInt(array[8]);
    printInt(array[9]);

   search =  435;
 
   first = 0;
   last = n - 1;
   middle = (first+last)/2;
 
   while (first <= last) {
      if (array[middle] < search)
         first = middle + 1;
      else if (array[middle] == search) {
         // printInt("%d found at location %d.\n", search, middle+1);
         printInt(middle+1);
         break;
      }
      else
         last = middle - 1;
 
      middle = (first + last)/2;
   }
   printInt(middle+1);
   // if (first > last)
   //    printf("Not found! %d is not present in the list.\n", search);
 
   return 0;   
}