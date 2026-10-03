from accumulator import AccumulatorCPU


class ProgramRunner:
    def __init__(self):
        self.cpu = AccumulatorCPU()

    def execute_instruction(self, instruction):
        operation = instruction[0]

        if operation == "LOAD":
            value = instruction[1]
            self.cpu.load(value)

        elif operation == "ADD":
            value = instruction[1]
            self.cpu.add(value)

        elif operation == "AND":
            value = instruction[1]
            self.cpu.and_value(value)

        elif operation == "OR":
            value = instruction[1]
            self.cpu.or_value(value)

        elif operation == "XOR":
            value = instruction[1]
            self.cpu.xor_value(value)

        elif operation == "NOT":
            self.cpu.not_acc()

        else:
            raise ValueError(
                f"Unknown instruction: {operation}"
            )

    def run(self, program):
        print("=== PROGRAM START ===")
        print()

        for address, instruction in enumerate(program):
            print(
                f"{address:02d}:",
                *instruction,
            )

            self.execute_instruction(
                instruction
            )

            value = self.cpu.read()

            print(
                f"    ACC = {value:04b} ({value})"
            )

        print()
        print("=== PROGRAM END ===")


def test_program():
    runner = ProgramRunner()

    program = [
        ("LOAD", 3),
        ("ADD", 10),
        ("ADD", 1),
        ("ADD", 1),
    ]

    for instruction in program:
        runner.execute_instruction(
            instruction
        )

    assert runner.cpu.read() == 15


def demo():
    program = [
        ("LOAD", 3),
        ("ADD", 10),
        ("ADD", 1),
        ("ADD", 1),
    ]

    runner = ProgramRunner()
    runner.run(program)


if __name__ == "__main__":
    test_program()

    print("All program tests passed.")
    print()

    demo()
