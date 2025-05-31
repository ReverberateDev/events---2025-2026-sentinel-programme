def remove_negatives(numbers):
    temp_list = list() # Declare an empty list to store non-negative numbers
    for number in numbers:
        # if number < 0: (We use the case such that only if the number is positive do we add it to the list)
        if number > 0: # Only add number if it is positive
            # numbers.remove(number)
            temp_list.append(number) # Adding number
    # return numbers (Don't return the original list)
    return temp_list # Return the new list with only positive numbers

numbers_list = [1, -2, 3, -4, -5, 6, -7, -8]
print(remove_negatives(numbers_list))  # Expected: [1, 3, 6]