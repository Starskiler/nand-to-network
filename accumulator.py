from alu import (
    OP_ADD,
    OP_AND,
    OP_OR,
    OP_XOR,
    OP_NOT,
)

from alu_hw import hardware_alu4
from memory import Register4


class AccumulatorCPU:
    def __init__(self):
        self.acc = Register4()

    def read(self):
        return self.acc.read()

    def load(self, value):
        """
        LOAD places a value directly into ACC.

        For now this is intentionally simplified.
        Later, a hardware multiplexer and instruction
        decoder will control this path.
        """

        self.acc.clock(value)

    def execute(self, opcode, operand=0):
        """
        ACC becomes input A of the ALU.

        operand becomes input B.

        ALU result is captured back into ACC
        on the simulated clock edge.
        """

        current = self.acc.read()

        result, flags = hardware_alu4(
            current,
            operand,
            opcode,
        )

        self.acc.clock(result)

        return result, flags

    def add(self, value):
        return self.execute(
            OP_ADD,
            value,
        )

    def and_value(self, value):
        return self.execute(
            OP_AND,
            value,
        )

    def or_value(self, value):
        return self.execute(
            OP_OR,
            value,
        )

    def xor_value(self, value):
        return self.execute(
            OP_XOR,
            value,
        )

    def not_acc(self):
        return self.execute(
            OP_NOT,
            0,
        )


def show(value):
    return f"{value:04b} ({value})"


def test_accumulator():
    cpu = AccumulatorCPU()

    cpu.load(3)
    assert cpu.read() == 3

    cpu.add(10)
    assert cpu.read() == 13

    cpu.add(1)
    assert cpu.read() == 14

    cpu.add(1)
    assert cpu.read() == 15

    cpu.xor_value(15)
    assert cpu.read() == 0

    cpu.not_acc()
    assert cpu.read() == 15


def demo():
    cpu = AccumulatorCPU()

    print("=== 4-BIT ACCUMULATOR CPU ===")
    print()

    print("LOAD 3")
    cpu.load(3)

    print(
        "ACC =",
        show(cpu.read()),
    )

    print()

    print("ADD 10")
    cpu.add(10)

    print(
        "ACC =",
        show(cpu.read()),
    )

    print()

    print("ADD 1")
    cpu.add(1)

    print(
        "ACC =",
        show(cpu.read()),
    )

    print()

    print("ADD 1")
    cpu.add(1)

    print(
        "ACC =",
        show(cpu.read()),
    )


if __name__ == "__main__":
    test_accumulator()

    print(
        "All accumulator tests passed."
    )

    print()

    demo()
