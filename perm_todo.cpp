#include <iostream>

//perm({a,b,c}) = a.perm({b,c}) + b.perm({a,c}) + c.perm({a,b}) 
            //= ab.perm({c}) + ac.perm({b}) + ba.perm({c}) + bc.perm({a}) + ca.perm({b}) + cb.perm({a})
            //= abc + acb + bac + bca + cab + cba

//perm({a,b,c,d}) = a.perm({b,c,d}) + b.perm({a,c,d}) + c.perm({a,b,d}) + d.perm({a,b,c})
            //= ab.perm({c}) + ac.perm({b}) + ba.perm({c}) + bc.perm({a}) + ca.perm({b}) + cb.perm({a})
            //= abc + acb + bac + bca + cab + cba
using namespace std;



void swap(int &x, int &y)
{
    int tmp;
    tmp = x;
    x = y;
    y = tmp;
}

void print_lst(int* lst)
{
    for (int i = 0; i < 4; i ++)
        cout << lst[i] << ",";
    cout << endl;    
}

void perm(int* lst, int k, int m)
{
    if (k == m)
        print_lst(lst);
    else
    {
        for (int i = k; i <= m; i++)
        {
            swap(lst[i], lst[k]);
            perm(lst, k + 1, m);
            swap(lst[i], lst[k]);
        }
    }
}



int main()
{
    //int x = 15, y = 20;
    //cout << x << " and " << y << endl;
    //swap(x, y);
    //cout << x << " and " << y << endl;
    //cout << "yes" << endl;



    //int lst[3] = {4, 5, 6};
    //print_lst(lst);
    //swap(lst[0], lst[2]);
    //print_lst(lst);
    int lst[4] = {4, 5, 6, 7};
    perm(lst, 0, 3);
    return 0;
}

