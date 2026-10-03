# NAND to Network

A learning project where I build a computer from the lowest logical level upward.

The goal is to start with a single universal logic gate — **NAND** — and progressively build:

```text
NAND
  ↓
Logic gates
  ↓
Adders
  ↓
ALU
  ↓
Memory
  ↓
Registers
  ↓
CPU
  ↓
Instruction set
  ↓
Assembler
  ↓
Machine code
  ↓
Operating system concepts
  ↓
Networking
```

## Current progress

### 1. Logic gates

Built from NAND:

- NOT
- AND
- OR
- XOR

### 2. Binary addition

Implemented:

- Half-adder
- Full-adder
- 4-bit ripple-carry adder

The full-adder handles:

```text
A + B + Carry In
```

and produces:

```text
Sum + Carry Out
```

### 3. 4-bit ALU

The ALU currently supports:

| Opcode | Operation |
|---|---|
| `000` | AND |
| `001` | OR |
| `010` | XOR |
| `011` | ADD |
| `100` | NOT A |

It also produces:

- `Z` — Zero flag
- `C` — Carry flag
- `N` — Negative/sign-bit flag

Operation selection is performed using NAND-based multiplexers.

### 4. Memory

Implemented a simplified model of:

- D flip-flop behavior
- 4-bit register
- Clocked state capture

The important distinction is:

```text
ALU      = computes the current result
Register = remembers a captured result
```

### 5. First CPU-style cycle

The ALU output can now be captured into a register:

```text
A / B
  ↓
 ALU
  ↓
Result
  ↓
Clock edge
  ↓
Register
```

The stored value can then be sent back into the ALU for another calculation.

Example:

```text
3 + 10 = 13
CLOCK
Register = 13

1 + 1 = 2
Register still = 13

CLOCK
Register = 2

Register + 3 = 5
CLOCK
Register = 5
```

This is the beginning of CPU state.

## Next step

Build an **accumulator-based CPU model**.

The accumulator will allow operations such as:

```text
LOAD 3
ADD 10
ADD 1
ADD 1
```

producing:

```text
3
13
14
15
```

After that, the project will progressively move toward:

- instruction decoding
- program counter
- RAM
- instruction execution
- machine code
- assembler
- a complete small CPU architecture

## Philosophy

The purpose of this project is not just to simulate a CPU with Python.

The goal is to understand why each component exists and how simple binary logic gradually becomes a programmable computer.
