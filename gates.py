def check_bit(value):
    if value not in (0, 1):
        raise ValueError("A bit must be 0 or 1")


# ============================================================
# THE ONLY PRIMITIVE GATE
# ============================================================

def nand(a, b):
    check_bit(a)
    check_bit(b)

    if a == 1 and b == 1:
        return 0

    return 1


# ============================================================
# EVERYTHING BELOW IS BUILT FROM NAND
# ============================================================

def not_gate(a):
    return nand(a, a)


def and_gate(a, b):
    return not_gate(
        nand(a, b)
    )


def or_gate(a, b):
    return nand(
        not_gate(a),
        not_gate(b),
    )


def xor_gate(a, b):
    ab = nand(a, b)

    return nand(
        nand(a, ab),
        nand(b, ab),
    )


# ============================================================
# ADDERS
# ============================================================

def half_adder(a, b):
    total = xor_gate(a, b)
    carry = and_gate(a, b)

    return total, carry


def full_adder(a, b, carry_in):
    first_sum, first_carry = half_adder(a, b)

    final_sum, second_carry = half_adder(
        first_sum,
        carry_in,
    )

    carry_out = or_gate(
        first_carry,
        second_carry,
    )

    return final_sum, carry_out


# ============================================================
# 4-BIT RIPPLE-CARRY ADDER
# ============================================================

def int_to_bits4(value):
    if not 0 <= value <= 15:
        raise ValueError("Value must fit in 4 bits")

    return [
        (value >> 0) & 1,
        (value >> 1) & 1,
        (value >> 2) & 1,
        (value >> 3) & 1,
    ]


def bits_to_int(bits):
    value = 0

    for index, bit in enumerate(bits):
        value |= bit << index

    return value


def add4(a, b):
    a_bits = int_to_bits4(a)
    b_bits = int_to_bits4(b)

    result_bits = []
    carry = 0

    for a_bit, b_bit in zip(
        a_bits,
        b_bits,
    ):
        result_bit, carry = full_adder(
            a_bit,
            b_bit,
            carry,
        )

        result_bits.append(
            result_bit
        )

    return bits_to_int(result_bits), carry


# ============================================================
# TESTS
# ============================================================

def test_gates():
    assert not_gate(0) == 1
    assert not_gate(1) == 0

    assert and_gate(0, 0) == 0
    assert and_gate(0, 1) == 0
    assert and_gate(1, 0) == 0
    assert and_gate(1, 1) == 1

    assert or_gate(0, 0) == 0
    assert or_gate(0, 1) == 1
    assert or_gate(1, 0) == 1
    assert or_gate(1, 1) == 1

    assert xor_gate(0, 0) == 0
    assert xor_gate(0, 1) == 1
    assert xor_gate(1, 0) == 1
    assert xor_gate(1, 1) == 0


def test_adder():
    for a in range(16):
        for b in range(16):
            result, carry = add4(a, b)

            expected = a + b

            assert result == expected & 0b1111
            assert carry == int(expected > 15)


def demo():
    examples = [
        (3, 5),
        (7, 6),
        (9, 4),
        (15, 1),
        (15, 15),
    ]

    print("=== 4-BIT NAND COMPUTER ===")
    print()

    for a, b in examples:
        result, carry = add4(a, b)

        print(
            f"{a:02d} + {b:02d}"
            f" -> result={result:02d}"
            f" carry={carry}"
        )


if __name__ == "__main__":
    test_gates()
    test_adder()

    print("All logic tests passed.")
    print()

    demo()
