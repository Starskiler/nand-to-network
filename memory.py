class DFlipFlop:
    def __init__(self):
        self.q = 0

    def clock(self, d):
        if d not in (0, 1):
            raise ValueError("D must be 0 or 1")

        self.q = d

    def read(self):
        return self.q


class Register4:
    def __init__(self):
        self.bits = [
            DFlipFlop(),
            DFlipFlop(),
            DFlipFlop(),
            DFlipFlop(),
        ]

    def clock(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Value must fit in 4 bits")

        bits = [
            (value >> 3) & 1,
            (value >> 2) & 1,
            (value >> 1) & 1,
            value & 1,
        ]

        for flip_flop, bit in zip(
            self.bits,
            bits,
        ):
            flip_flop.clock(bit)

    def read_bits(self):
        return [
            flip_flop.read()
            for flip_flop in self.bits
        ]

    def read(self):
        value = 0

        for bit in self.read_bits():
            value = (value << 1) | bit

        return value


def demo():
    register = Register4()

    print("=== 4-BIT REGISTER ===")
    print()

    print(
        f"Initial: {register.read():04b}"
    )

    print()
    print("On prépare D = 1010")
    print("Mais sans clock, Q ne change pas.")
    print(
        f"Q = {register.read():04b}"
    )

    register.clock(0b1010)

    print()
    print("CLOCK ↑")
    print(
        f"Q = {register.read():04b}"
    )

    print()
    print("On prépare ensuite D = 0011")
    print("Toujours aucune clock.")
    print(
        f"Q = {register.read():04b}"
    )

    register.clock(0b0011)

    print()
    print("CLOCK ↑")
    print(
        f"Q = {register.read():04b}"
    )


if __name__ == "__main__":
    demo()
