#include <iostream>

using namespace std;

void print_lst(int* lst)
{
    for (int i=0; i<4; i++)
        cout << lst[i] << ",";
    cout << endl;
}

void swap(int &x, int &y)
{
    int tmp = x;
    x = y;
    y = tmp;
}

void perm(int* lst, int k, int m)
{
    if (k == m)
        print_lst(lst);
    else
    {
        for (int i=k; i<=m; i++)
        {
            swap(lst[i], lst[k]);
            perm(lst, k + 1, m);
            swap(lst[i], lst[k]);
        }
    }
}



int main()
{
    int lst[4] = {2,3,4,5};
    perm(lst, 0, 3);
    return 0;
}
