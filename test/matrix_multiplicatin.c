int main()
{
  int m, n, p, q, c, d, k, sum = 0;
  int first[2][2], second[2][2], multiply[2][2];
  m = 2;
  n = 2;
  p = 2;
  q = 2;
  
  for (c = 0; c < m; c++)
    for (d = 0; d < n; d++)
 		first[c][d] = 1;
 
    for (c = 0; c < p; c++)
      for (d = 0; d < q; d++)
 		second[c][d] = 2;

    for (c = 0; c < m; c++) {
      for (d = 0; d < q; d++) {
        for (k = 0; k < p; k++) {
          sum = sum + first[c][k]*second[k][d];
        } 
        multiply[c][d] = sum;
        sum = 0;
      }
    }
  
    for (c = 0; c < m; c++) {
      for (d = 0; d < q; d++){
      	int temp = multiply[c][d];
        printInt(multiply[c][d]);
    }
    }
 
  return 0;
}