from prime import is_prime


def test_prime(x, expected):
    if is_prime(x) != expected:
        print(f"ERROR on is_prime({x}), expected={expected}")
