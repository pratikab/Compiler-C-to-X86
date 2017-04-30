int main()
{
    int i, n, t1 = 0, t2 = 1, nextTerm = 0;

    n = 5;


    for (i = 1; i <= n; i++)
    {
        // Prints the first two terms.
        if(i == 1)
        {
            printInt(t1);
            continue;
        }
        if(i == 2)
        {
            printInt(t2);
            continue;
        }
        nextTerm = t1 + t2;
        t1 = t2;
        t2 = nextTerm;
        printInt(nextTerm);
    }
    return 0;
}