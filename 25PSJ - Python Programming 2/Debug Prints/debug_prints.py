def remove_books_by_author(inventory, 
author_to_remove):
    """
    Attempts to remove all books by a specified 
author from the inventory.
    Parameters:
    - inventory: List of dictionaries, where 
each dictionary represents a book with 'title' 
and 'author'.
    - author_to_remove: String, the name of the 
author whose books should be removed.
    """
    temp_list = list() # Declare a temporary dictionary to store books that are not by the specified author
    for index in range(len(inventory)):
        # if inventory[index]['author'] == author_to_remove: (Wont need this anymore)
        if inventory[index]['author'] != author_to_remove: # Only add books not by the specified author
            # del inventory[index] (This is the line that causes the issue)
            temp_list.append(inventory[index]) # Add books not by the specified author
    # return inventory (We will not need this anymore)
    return temp_list # Return the new list with only books not by the specified author
# Example inventory with more realistic book titles 
inventory = [
    {'title': 'Shadows of Tomorrow', 'author': 
'John Doe'},
    {'title': 'The Last Chronicle', 'author': 
'Jane Smith'},
    {'title': 'Echoes of the Past', 'author': 
'John Doe'},
    {'title': 'The Silent Forest', 'author': 
'Emily Jones'},
    {'title': 'Beyond the Horizon', 'author': 
'John Doe'},
    {'title': 'Whispers of the Ancient', 
'author': 'John Doe'},
    {'title': 'Under the Moonlight', 'author': 
'Michael Brown'}
]
# Author to remove
author_to_remove = 'John Doe'
# Attempt to remove books by the specified author
updated_inventory = remove_books_by_author(inventory, author_to_remove)
print("Updated Inventory:")
for book in updated_inventory:
    print(f"- {book['title']} by {book['author']}")