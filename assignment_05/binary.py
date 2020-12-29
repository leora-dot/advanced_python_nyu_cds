import itertools

"""
Write a program that takes two arguments n and k and prints all binary strings of length n that contain k zero bits, one per line.
"""

def zbits(n, k):
    num_ones = n-k
    products = itertools.product(range(2), repeat=n)
    tups = [prod for prod in products if sum(prod) == num_ones]

    for tup in tups:
        print(''.join(str(x) for x in tup))

##TESTING

#zbits(4,3)
#zbits(4,1)
#zbits(5,4)
