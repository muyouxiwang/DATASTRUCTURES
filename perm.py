# -*- coding=utf-8 -*-

#perm({a,b,c}) = a.perm({b,c}) + b.perm({a,c}) + c.perm({a,b}) 
            #= ab.perm({c}) + ac.perm({b}) + ba.perm({c}) + bc.perm({a}) + ca.perm({b}) + cb.perm({a})
            #= abc + acb + bac + bca + cab + cba

#perm({a,b,c,d}) = a.perm({b,c,d}) + b.perm({a,c,d}) + c.perm({a,b,d}) + d.perm({a,b,c})
            #= ab.perm({c}) + ac.perm({b}) + ba.perm({c}) + bc.perm({a}) + ca.perm({b}) + cb.perm({a})
            #= abc + acb + bac + bca + cab + cba


#void perm(int* lst, int k, int m)
#{
#    if (k == m)
#        print_lst(lst);
#    else
#    {
#        for (int i = k; i <= m; i++)
#        {
#            swap(lst[i], lst[k]);
#            perm(lst, k + 1, m);
#            swap(lst[i], lst[k]);
#        }
#    }
#}

def perm(lst, k, m):
    if k == m:
        print lst
        


def main():
    lst = [4, 5, 6];
    perm(lst, 0, len(lst) - 1)


if __name__ == "__main__":
    main()


