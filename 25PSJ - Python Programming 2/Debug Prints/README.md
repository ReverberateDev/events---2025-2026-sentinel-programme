Traceback (most recent call last):
  File "c:\Users\rapha\Raphael Lim\Extra Curricular\Events\sentinel-programme\Debug Prints\debug_prints.py", line 37, in <module>
    updated_inventory = remove_books_by_author(inventory, author_to_remove)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Users\rapha\Raphael Lim\Extra Curricular\Events\sentinel-programme\Debug Prints\debug_prints.py", line 14, in remove_books_by_author
    if inventory[index]['author'] == author_to_remove:
       ~~~~~~~~~^^^^^^^
IndexError: list index out of range

The above was the error that occured when the initail program ran

It can be seen that the index is out of range of the list, this is because the list of modified as the program, for e.g. if we are at index 2, but we delete index 2, the list will be compressed such that the element initially at index 3 will be shifted to index 2, yet len(inventory) is called at the start, which causes index to reach a number that will ever be more than what the list has

Instead of removing books by the specified book, we can just create an answer list with books that are not by the author we don't want