def is_even(number):
    # if number % 2 == 1: (If the number is even, the remainder of the number when divided by 2 should be 0, not 1)
    if number % 2 == 0:
        return True
    else:
        return False

print(is_even(4)) # 4 should be even