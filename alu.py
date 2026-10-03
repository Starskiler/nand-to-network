from gates import (
    add4,
    and_gate,
    bits_to_int,
    int_to_bits4,
    not_gate,
    or_gate,
    xor_gate,
)


# ============================================================
# OPCODES
# ============================================================

OP_AND = 0b000
OP_OR = 0b001
OP_XOR = 0b010
OP_ADD = 0b011
OP_NOT = 0b100


OPCODE_NAMES = {
    OP_AND: "AND",
    OP_OR: "OR",
    OP_XOR: "XOR",
    OP_ADD: "ADD",
    OP_NOT: "NOT",
}


# ============================================================
# 4-BIT LOGIC OPERATIONS
# ============================================================

def binary_gate4(a, b, gate):
    a_bits = int_to_bits4(a)
    b_bits = int_to_bits4(b)

    result_bits = []

    for a_bit, b_bit in zip(
        a_bits,
        b_bits,
    ):
        result_bits.append(
            gate(a_bit, b_bit)
        )

    return bits_to_int(result_bits)


def and4(a, b):
    return binary_gate4(
        a,
        b,
        and_gate,
    )


def or4(a, b):
    return binary_gate4(
        a,
        b,
        or_gate,
    )


def xor4(a, b):
    return binary_gate4(
        a,
        b,
        xor_gate,
    )


def not4(a):
    a_bits = int_to_bits4(a)

    result_bits = [
        not_gate(bit)
        for bit in a_bits
    ]

    return bits_to_int(result_bits)


# ============================================================
# FLAGS
# ============================================================

def zero_flag4(value):
    bits = int_to_bits4(value)

    low_pair = or_gate(
        bits[0],
        bits[1],
    )

    high_pair = or_gate(
        bits[2],
        bits[3],
    )

    any_high = or_gate(
        low_pair,
        high_pair,
    )

    return not_gate(any_high)


def negative_flag4(value):
    bits = int_to_bits4(value)

    return bits[3]


def make_flags(
    result,
    carry=0,
):
    return {
        "zero": zero_flag4(result),
        "carry": carry,
        "negative": negative_flag4(result),
    }


# ============================================================
# ALU
# ============================================================

def alu4(
    a,
    b,
    opcode,
):
    if opcode == OP_AND:
        result = and4(a, b)
        carry = 0

    elif opcode == OP_OR:
        result = or4(a, b)
        carry = 0

    elif opcode == OP_XOR:
        result = xor4(a, b)
        carry = 0

    elif opcode == OP_ADD:
        result, carry = add4(a, b)

    elif opcode == OP_NOT:
        result = not4(a)
        carry = 0

    else:
        raise ValueError(
            f"Unknown opcode: {opcode:03b}"
        )

    return (
        result,
        make_flags(
            result,
            carry,
        ),
    )


# ============================================================
# TESTS
# ============================================================

def test_logic_operations():
    for a in range(16):
        for b in range(16):
            assert and4(a, b) == (a & b)
            assert or4(a, b) == (a | b)
            assert xor4(a, b) == (a ^ b)

        assert not4(a) == ((~a) & 0b1111)


def test_alu():
    for a in range(16):
        for b in range(16):

            result, flags = alu4(
                a,
                b,
                OP_AND,
            )

            assert result == (a & b)

            result, flags = alu4(
                a,
                b,
                OP_OR,
            )

            assert result == (a | b)

            result, flags = alu4(
                a,
                b,
                OP_XOR,
            )

            assert result == (a ^ b)

            result, flags = alu4(
                a,
                b,
                OP_ADD,
            )

            expected = a + b

            assert result == (
                expected & 0b1111
            )

            assert flags["carry"] == int(
                expected > 15
            )

            assert flags["zero"] == int(
                result == 0
            )

            assert flags["negative"] == (
                (result >> 3) & 1
            )


def test_not():
    for a in range(16):
        result, flags = alu4(
            a,
            0,
            OP_NOT,
        )

        assert result == (
            (~a) & 0b1111
        )


# ============================================================
# DEMO
# ============================================================

def demo_operation(
    a,
    b,
    opcode,
):
    result, flags = alu4(
        a,
        b,
        opcode,
    )

    name = OPCODE_NAMES[opcode]

    print(
        f"{name:3} | "
        f"A={a:04b} "
        f"B={b:04b} "
        f"-> {result:04b} "
        f"| Z={flags['zero']} "
        f"C={flags['carry']} "
        f"N={flags['negative']}"
    )


def demo():
    print("=== NAND-BASED 4-BIT ALU ===")
    print()

    demo_operation(
        0b1100,
        0b1010,
        OP_AND,
    )

    demo_operation(
        0b1100,
        0b1010,
        OP_OR,
    )

    demo_operation(
        0b1100,
        0b1010,
        OP_XOR,
    )

    demo_operation(
        0b0111,
        0b0011,
        OP_ADD,
    )

    demo_operation(
        0b1111,
        0b0001,
        OP_ADD,
    )

    demo_operation(
        0b0101,
        0,
        OP_NOT,
    )


if __name__ == "__main__":
    test_logic_operations()
    test_alu()
    test_not()

    print("All ALU tests passed.")
    print()

    demo()
