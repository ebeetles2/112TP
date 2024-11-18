def test_function(a, n):
    for i in range(len(a)):
        if a[i] == n:
            return i

a = [1, 2, 3, 4, 5]
n = 3
z = test_function(a, n)
