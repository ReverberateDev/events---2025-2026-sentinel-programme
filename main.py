with open("secret.txt", "r", encoding="utf-8") as file:
    a, b, c = 0, 0, 0
    lines = file.readlines()
    for line in lines:
        line = line.rstrip('\n')  # Corrected the newline strip
        if len(line) == 13:
            b += 1
        if line.isnumeric():
            number = int(line)
            if number % 2 == 0:
                a += number
            else:
                c += number
    # Instead of concatenating strings, using a format for clarity
    print(f"{a}{b}{c}")
