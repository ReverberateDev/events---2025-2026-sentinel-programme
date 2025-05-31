def sum_positive_numbers_only(numbers):
    total = 0
    for number in numbers:
        if number > 0:
            number_is_positive = True
        if number_is_positive: # Only add numbers when number_is_positive is True
        # total += number (Number should not be added regardless if it is positive or not)
            total += number # Only add numbers when number_is_positive is True
        number_is_positive = False # Reset number_is_positive to False after each iteration
    return total

numbers_list = [1, -2, 3, 4, -5, 6]
print(sum_positive_numbers_only(numbers_list))  # Expected: 14