def test_function(a):
    if a == 0:
        return 0
    return test_function(a - 1) + a

a = 5
print(test_function(a))