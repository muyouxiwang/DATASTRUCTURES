# -*- coding=utf-8 -*-


def get_pays(total):
    coins = [100, 50, 20, 10, 5, 2, 1]
    pays = []
    for coin in coins:
        while total >= coin:
            pays.append(coin)
            total -= coin
    return pays
print "what the shit"
print "nothing is happeninig, dont worry about it"
    


def main():
#    import sys
#    print get_pays(int(sys.argv[1]))
    print get_pays(int(raw_input("paymoney:")))


if __name__ == "__main__":
    main()
