from math import factorial
import sys

while True:
    str = sys.stdin.readline()
    str = str.rstrip()
    # print(str)
    if str != '':
        elems = set(str)
        results = {}
        for elem in elems:
            results[elem] = str.count(elem)
        num = factorial(len(str))
        denum = 1
        for elem in results:
            denum *= factorial(results[elem])
        print(num // denum)
        #print(int(num // denum))
        # print("num {0}, denum {1}".format(num, denum))
        # if not str:
        #     break
    else:
        break

