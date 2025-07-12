import sys

def main():
    total_sum = 0.0
    arguments = sys.argv[1:]

    if not arguments:
        print("Total sum: 0.0")
        return

    for arg in arguments:
        try:
            number = float(arg)
            total_sum += number
        except ValueError:
            print(f"Warning: '{arg}' is not a number and will be ignored.")
    
    print(f"Total sum: {total_sum}")

if __name__ == "__main__":
    main()