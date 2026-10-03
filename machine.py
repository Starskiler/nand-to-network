from accumulator import AccumulatorCPU
from program_counter import ProgramCounter


class Machine:
    def __init__(self, program):
        self.program = program

        self.cpu = AccumulatorCPU()
        self.pc = ProgramCounter()

    def fetch(self):
        """
        Use PC as the address of the next instruction.
        """

        address = self.pc.read()

        if address >= len(self.program):
            return None

        return self.program[address]

    def execute(self, instruction):
        """
        Execute one decoded instruction.
        """

        operation = instruction[0]

        if operation == "LOAD":
            self.cpu.load(
                instruction[1]
            )

        elif operation == "ADD":
            self.cpu.add(
                instruction[1]
            )

        elif operation == "AND":
            self.cpu.and_value(
                instruction[1]
            )

        elif operation == "OR":
            self.cpu.or_value(
                instruction[1]
            )

        elif operation == "XOR":
            self.cpu.xor_value(
                instruction[1]
            )

        elif operation == "NOT":
            self.cpu.not_acc()

        else:
            raise ValueError(
                f"Unknown instruction: {operation}"
            )

    def step(self):
        """
        Execute exactly one instruction.
        """

        address = self.pc.read()

        instruction = self.fetch()

        if instruction is None:
            return False

        print(
            f"PC={address:04b} ({address})"
        )

        print(
            "FETCH:",
            *instruction,
        )

        self.execute(
            instruction
        )

        print(
            f"ACC={self.cpu.read():04b} "
            f"({self.cpu.read()})"
        )

        self.pc.increment()

        print(
            f"NEXT PC={self.pc.read():04b} "
            f"({self.pc.read()})"
        )

        print()

        return True

    def run(self):
        print("=== MACHINE START ===")
        print()

        while self.step():
            pass

        print("=== MACHINE HALTED ===")

        print(
            f"FINAL ACC={self.cpu.read():04b} "
            f"({self.cpu.read()})"
        )


def test_machine():
    program = [
        ("LOAD", 3),
        ("ADD", 10),
        ("ADD", 1),
        ("ADD", 1),
    ]

    machine = Machine(program)

    machine.run()

    assert machine.cpu.read() == 15
    assert machine.pc.read() == 4


def demo():
    program = [
        ("LOAD", 3),
        ("ADD", 10),
        ("ADD", 1),
        ("ADD", 1),
    ]

    machine = Machine(program)

    machine.run()


if __name__ == "__main__":
    test_machine()

    print()
    print("All machine tests passed.")
    print()

    demo()
