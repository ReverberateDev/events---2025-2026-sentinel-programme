def remove_books_by_author(inventory,
author_to_remove):
    """
    Removes all books by a specified author
    from the inventory.
    Parameters:
    - inventory: List of dictionaries, where
    each dictionary represents a book with 'title'
    and 'author'.
    - author_to_remove: String, the name of the
    author whose books should be removed.
    """
    # for book in inventory: We won't need this anymore
    #    if book['author'] == author_to_remove:
    #        inventory.remove(book)
    # return inventory
    return [book for book in inventory if book['author'] != author_to_remove]
    # Essentially, this line creates a new list that contains only the books whose author is not the one we want to remove.
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
# Remove books by the specified author
updated_inventory = remove_books_by_author(inventory, author_to_remove)
print("Updated Inventory:")
for book in updated_inventory:
    print(f"- {book['title']} by {book['author']}")