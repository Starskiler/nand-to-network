from gates import (
    int_to_bits4,
    bits_to_int,
    nand,
    not_gate,
)

from alu import (
    and4,
    or4,
    xor4,
    not4,
    add4,
    make_flags,
)


# ============================================================
# 1-BIT MULTIPLEXER
# ============================================================

def mux1(a, b, select):
    """
    select = 0 -> A
    select = 1 -> B

    Built only from NAND + NOT,
    and NOT itself is already built from NAND.
    """

    not_select = not_gate(select)

    a_path = nand(
        a,
        not_select,
    )

    b_path = nand(
        b,
        select,
    )

    return nand(
        a_path,
        b_path,
    )


# ============================================================
# 4-BIT MULTIPLEXER
# ============================================================

def mux4(
    a,
    b,
    select,
):
    a_bits = int_to_bits4(a)
    b_bits = int_to_bits4(b)

    result_bits = []

    for a_bit, b_bit in zip(
        a_bits,
        b_bits,
    ):
        result_bits.append(
            mux1(
                a_bit,
                b_bit,
                select,
            )
        )

    return bits_to_int(
        result_bits
    )


# ============================================================
# 8-WAY / 1-BIT MULTIPLEXER
# ============================================================

def mux8_1(
    v0,
    v1,
    v2,
    v3,
    v4,
    v5,
    v6,
    v7,
    s0,
    s1,
    s2,
):
    """
    Three selector bits choose one of eight inputs.

    s2 s1 s0

    000 -> v0
    001 -> v1
    010 -> v2
    011 -> v3
    100 -> v4
    101 -> v5
    110 -> v6
    111 -> v7
    """

    level1_0 = mux1(v0, v1, s0)
    level1_1 = mux1(v2, v3, s0)
    level1_2 = mux1(v4, v5, s0)
    level1_3 = mux1(v6, v7, s0)

    level2_0 = mux1(
        level1_0,
        level1_1,
        s1,
    )

    level2_1 = mux1(
        level1_2,
        level1_3,
        s1,
    )

    return mux1(
        level2_0,
        level2_1,
        s2,
    )


# ============================================================
# 8-WAY / 4-BIT MULTIPLEXER
# ============================================================

def mux8_4(
    v0,
    v1,
    v2,
    v3,
    v4,
    v5,
    v6,
    v7,
    s0,
    s1,
    s2,
):
    level1_0 = mux4(v0, v1, s0)
    level1_1 = mux4(v2, v3, s0)
    level1_2 = mux4(v4, v5, s0)
    level1_3 = mux4(v6, v7, s0)

    level2_0 = mux4(
        level1_0,
        level1_1,
        s1,
    )

    level2_1 = mux4(
        level1_2,
        level1_3,
        s1,
    )

    return mux4(
        level2_0,
        level2_1,
        s2,
    )


# ============================================================
# HARDWARE ALU
# ============================================================

def hardware_alu4(
    a,
    b,
    opcode,
):
    if not 0 <= opcode <= 7:
        raise ValueError(
            "Opcode must fit in 3 bits"
        )

    opcode_bits = int_to_bits4(
        opcode
    )

    s0 = opcode_bits[0]
    s1 = opcode_bits[1]
    s2 = opcode_bits[2]

    # IMPORTANT:
    #
    # The ALU computes EVERY possible operation.
    # Then the multiplexer chooses which electrical
    # result is connected to the output.

    result_and = and4(a, b)
    result_or = or4(a, b)
    result_xor = xor4(a, b)

    result_add, carry_add = add4(
        a,
        b,
    )

    result_not = not4(a)

    # 000 AND
    # 001 OR
    # 010 XOR
    # 011 ADD
    # 100 NOT
    #
    # 101 / 110 / 111 are currently unused.
    # Their hardware output is wired to 0000.

    result = mux8_4(
        result_and,
        result_or,
        result_xor,
        result_add,
        result_not,
        0,
        0,
        0,
        s0,
        s1,
        s2,
    )

    # Carry exists only for ADD.
    #
    # Again: no opcode comparison.
    # A multiplexer physically routes the correct carry.

    carry = mux8_1(
        0,
        0,
        0,
        carry_add,
        0,
        0,
        0,
        0,
        s0,
        s1,
        s2,
    )

    flags = make_flags(
        result,
        carry,
    )

    return result, flags


# ============================================================
# TESTS
# ============================================================

def test_mux1():
    assert mux1(0, 0, 0) == 0
    assert mux1(0, 1, 0) == 0
    assert mux1(1, 0, 0) == 1
    assert mux1(1, 1, 0) == 1

    assert mux1(0, 0, 1) == 0
    assert mux1(0, 1, 1) == 1
    assert mux1(1, 0, 1) == 0
    assert mux1(1, 1, 1) == 1


def expected_result(
    a,
    b,
    opcode,
):
    if opcode == 0:
        return a & b, 0

    if opcode == 1:
        return a | b, 0

    if opcode == 2:
        return a ^ b, 0

    if opcode == 3:
        total = a + b

        return (
            total & 0b1111,
            int(total > 15),
        )

    if opcode == 4:
        return (
            (~a) & 0b1111,
            0,
        )

    return 0, 0


def test_hardware_alu():
    for opcode in range(8):
        for a in range(16):
            for b in range(16):

                result, flags = hardware_alu4(
                    a,
                    b,
                    opcode,
                )

                expected, expected_carry = (
                    expected_result(
                        a,
                        b,
                        opcode,
                    )
                )

                assert result == expected

                assert flags["carry"] == (
                    expected_carry
                )

                assert flags["zero"] == int(
                    result == 0
                )

                assert flags["negative"] == (
                    (result >> 3) & 1
                )


# ============================================================
# DEMO
# ============================================================

NAMES = {
    0b000: "AND",
    0b001: "OR",
    0b010: "XOR",
    0b011: "ADD",
    0b100: "NOT",
    0b101: "---",
    0b110: "---",
    0b111: "---",
}


def demo():
    print(
        "=== HARDWARE-SELECTED 4-BIT ALU ==="
    )

    print()

    a = 0b1100
    b = 0b1010

    for opcode in range(8):
        result, flags = hardware_alu4(
            a,
            b,
            opcode,
        )

        print(
            f"{opcode:03b} "
            f"{NAMES[opcode]:3} | "
            f"A={a:04b} "
            f"B={b:04b} "
            f"-> {result:04b} "
            f"| "
            f"Z={flags['zero']} "
            f"C={flags['carry']} "
            f"N={flags['negative']}"
        )


if __name__ == "__main__":
    test_mux1()
    test_hardware_alu()

    print(
        "All hardware ALU tests passed."
    )

    print()

    demo()
