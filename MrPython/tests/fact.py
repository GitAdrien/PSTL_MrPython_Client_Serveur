
def fact(n):
    """doc"""
    
    # r : Number
    r = 1

    # i : int
    i = 2

    while i <= n:
        r = r * i
        i = i + 1
        print("i="+str(i))

    return r
i = 42
fact(5)



