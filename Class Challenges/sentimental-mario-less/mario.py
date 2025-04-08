def main():
    height = get_height()

    for row in range(height):
        print(" " * (height - row - 1), end="")
        print("#" * (row + 1))


def get_height():
    while True:
        try:
            height = int(input("Enter height here: "))
            if 1 <= height <= 8:
                return height
        except ValueError:
            pass


if __name__ == "__main__":
    main()
