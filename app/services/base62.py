# CHARACTER SET
# Sequence: [a-z] / [A-Z] / [0-9]
BASE62_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def encode(number: int):
    """
    Converts an integer into its base62 string representation, using BASE62_ALPHABET as the digit set
    """
    digits = []

    def divide(n):
        q = n // 62
        r = n % 62

        digits.append(r)

        if q > 0:
            divide(q)

    divide(number)

    digits.reverse()

    short_code = ""
    for pos in digits:
        short_code += BASE62_ALPHABET[pos]

    return short_code