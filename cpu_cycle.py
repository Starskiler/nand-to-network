from alu import OP_ADD
from alu_hw import hardware_alu4
from memory import Register4


class MiniCPU:
    def __init__(self):
        self.register = Register4()

    def calculate(self, a, b, opcode):
        """
        L'ALU calcule immédiatement.
        Rien n'est encore mémorisé.
        """
        return hardware_alu4(
            a,
            b,
            opcode,
        )

    def clock(self, a, b, opcode):
        """
        Front de clock :
        on capture la sortie ACTUELLE de l'ALU
        dans le registre.
        """
        result, flags = self.calculate(
            a,
            b,
            opcode,
        )

        self.register.clock(result)

        return flags

    def read_register(self):
        return self.register.read()


def show(value):
    return f"{value:04b} ({value})"


def demo():
    cpu = MiniCPU()

    print("=== FIRST CPU CYCLES ===")
    print()

    # --------------------------------------------------------
    # CYCLE 1
    # --------------------------------------------------------

    a = 0b0011      # 3
    b = 0b1010      # 10

    result, flags = cpu.calculate(
        a,
        b,
        OP_ADD,
    )

    print("1) ALU calcule 3 + 10")
    print("ALU      =", show(result))
    print(
        "REGISTER =",
        show(cpu.read_register()),
    )

    print()
    print("Pas encore de clock.")
    print("Le registre n'a donc rien copié.")

    cpu.clock(
        a,
        b,
        OP_ADD,
    )

    print()
    print("CLOCK ↑")

    print(
        "REGISTER =",
        show(cpu.read_register()),
    )

    # --------------------------------------------------------
    # CYCLE 2
    # --------------------------------------------------------

    print()
    print("-----------------------------")
    print()

    a = 0b0001
    b = 0b0001

    result, flags = cpu.calculate(
        a,
        b,
        OP_ADD,
    )

    print("2) Les entrées changent : 1 + 1")
    print("ALU      =", show(result))

    print(
        "REGISTER =",
        show(cpu.read_register()),
    )

    print()
    print(
        "L'ALU a changé, "
        "mais le registre garde 13."
    )

    cpu.clock(
        a,
        b,
        OP_ADD,
    )

    print()
    print("CLOCK ↑")

    print(
        "REGISTER =",
        show(cpu.read_register()),
    )

    # --------------------------------------------------------
    # CYCLE 3
    # --------------------------------------------------------

    print()
    print("-----------------------------")
    print()

    previous = cpu.read_register()

    result, flags = cpu.calculate(
        previous,
        0b0011,
        OP_ADD,
    )

    print(
        "3) On réutilise la valeur mémorisée."
    )

    print(
        "REGISTER précédent =",
        show(previous),
    )

    print("On calcule REGISTER + 3")
    print("ALU =", show(result))

    cpu.clock(
        previous,
        0b0011,
        OP_ADD,
    )

    print()
    print("CLOCK ↑")

    print(
        "NOUVEAU REGISTER =",
        show(cpu.read_register()),
    )


if __name__ == "__main__":
    demo()
