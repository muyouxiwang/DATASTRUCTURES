# -*- coding=utf-8 -*-

#import functools

#def mywrap(f):
#    cache = {}
#    @functools.wraps(f)
#    def wrap(*arg):
#        if arg not in cache:
#            cache[arg] = f(*arg)
#        return cache[arg]
#    return wrap

def mywrap(f):
    cache = {}
    def wrap(*arg):
        if arg not in cache:
            cache[arg] = f(*arg)
        return cache[arg]
    return wrap


@mywrap
def fib(n):
    if n==1 or n==2:
        return 1
    return fib(n-1) + fib(n-2)


def main():
    print fib(int(raw_input("input index of series:")))


if __name__ == "__main__":
    main()
