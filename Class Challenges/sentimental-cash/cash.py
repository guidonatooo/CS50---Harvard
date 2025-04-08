def get_cents():
    while True:
        try:
            cents = float(input("Cents Owed: "))
            if cents >= 0:
                return round(cents * 100)
        except ValueError:
            pass


def calculate_quarters(cents):
    quarters = 0
    while cents >= 25:
        cents -= 25
        quarters += 1
    return quarters


def calculate_dimes(cents):
    dimes = 0
    while cents >= 10:
        cents -= 10
        dimes += 1
    return dimes


def calculate_nickels(cents):
    nickels = 0
    while cents >= 5:
        cents -= 5
        nickels += 1
    return nickels


def calculate_pennies(cents):
    pennies = 0
    while cents >= 1:
        cents -= 1
        pennies += 1
    return pennies


def main():
    cents = get_cents()

    quarters = calculate_quarters(cents)
    cents -= quarters * 25

    dimes = calculate_dimes(cents)
    cents -= dimes * 10

    nickels = calculate_nickels(cents)
    cents -= nickels * 5

    pennies = calculate_pennies(cents)
    cents -= pennies * 1

    coins = quarters + dimes + nickels + pennies
    print(coins)


if __name__ == "__main__":
    main()
