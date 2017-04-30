int main()
{
  int array[100], n, c, d, swap, t;
 
  n=10;
  
  for (c = 0; c < n; c++)
    array[c] = 10 - c;
 
  for (c = 0 ; c < ( n - 1 ); c++)
  {
    for (d = 0 ; d < (n - c - 1); d++)
    {
      t = d+1;
      if (array[d] > array[t]) /* For decreasing order use < */
      {
        swap       = array[d];
        array[d]   = array[t];
        array[t] = swap;
      }
    }
  }
  
  for ( c = 0 ; c < n ; c++ )
     printInt(array[c]);
 
  return 0;
}