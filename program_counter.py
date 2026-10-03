from alu import OP_ADD
from alu_hw import hardware_alu4
from memory import Register4


class ProgramCounter:
    def __init__(self):
        self.register = Register4()

    def read(self):
        return self.register.read()

    def reset(self):
        self.register.clock(0)

    def load(self, value):
        if not 0 <= value <= 15:
            raise ValueError(
                "PC value must fit in 4 bits"
            )

        self.register.clock(value)

    def increment(self):
        current = self.read()

        result, flags = hardware_alu4(
            current,
            1,
            OP_ADD,
        )

        self.register.clock(result)

        return flags


def show(value):
    return f"{value:04b} ({value})"


def test_program_counter():
    pc = ProgramCounter()

    assert pc.read() == 0

    pc.increment()
    assert pc.read() == 1

    pc.increment()
    assert pc.read() == 2

    pc.load(14)
    assert pc.read() == 14

    pc.increment()
    assert pc.read() == 15

    flags = pc.increment()

    # 4-bit overflow:
    # 1111 + 1 = 0000 with carry
    assert pc.read() == 0
    assert flags["carry"] == 1

    pc.load(7)
    assert pc.read() == 7

    pc.reset()
    assert pc.read() == 0


def demo():
    pc = ProgramCounter()

    print("=== 4-BIT PROGRAM COUNTER ===")
    print()

    print(
        "Initial PC =",
        show(pc.read()),
    )

    for _ in range(5):
        current = pc.read()

        print()
        print(
            "Execute instruction at address",
            current,
        )

        pc.increment()

        print(
            "Next PC =",
            show(pc.read()),
        )

    print()
    print("--- Overflow demo ---")

    pc.load(15)

    print(
        "PC =",
        show(pc.read()),
    )

    flags = pc.increment()

    print("PC + 1")

    print(
        "PC =",
        show(pc.read()),
    )

    print(
        "Carry =",
        flags["carry"],
    )


if __name__ == "__main__":
    test_program_counter()

    print(
        "All program counter tests passed."
    )

    print()

    demo()
