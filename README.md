# NAND to Network

A learning project where I build a computer from the lowest logical level upward.

The goal is to start with a single universal logic gate — **NAND** — and progressively build enough hardware concepts to reach a programmable CPU, machine code, an assembler, operating-system concepts, and eventually networking.

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
Accumulator
  ↓
Program Counter
  ↓
Fetch / Execute cycle
  ↓
Machine code
  ↓
Instruction decoder
  ↓
RAM
  ↓
CPU architecture
  ↓
Assembler
  ↓
Operating-system concepts
  ↓
Networking
```

## Current status

The project currently has a working 4-bit educational CPU model with:

- NAND as the original primitive gate
- NOT, AND, OR and XOR
- Half-adder and full-adder
- 4-bit ripple-carry addition
- 4-bit ALU
- NAND-based multiplexers
- Zero, Carry and Negative flags
- Clocked 4-bit register
- Accumulator
- Program Counter
- Sequential programs
- Fetch / execute cycle

The current program representation is still symbolic Python data such as:

```text
LOAD 3
ADD 10
ADD 1
ADD 1
```

The next major step is to replace these symbolic instructions with binary machine instructions.

---

## 1. Logic gates

`gates.py` begins with NAND and builds the other required gates from it.

Implemented gates:

- `NAND`
- `NOT`
- `AND`
- `OR`
- `XOR`

The project uses NAND because it is a **universal gate**: all of the other logic used here can be constructed from NAND gates.

---

## 2. Binary addition

The first arithmetic component is the half-adder.

For two input bits:

```text
SUM   = A XOR B
CARRY = A AND B
```

A full-adder extends this to:

```text
A + B + Carry In
```

and produces:

```text
Sum + Carry Out
```

Several full-adders are chained together to create a 4-bit ripple-carry adder.

Example:

```text
  0011
+ 1010
------
  1101
```

which is:

```text
3 + 10 = 13
```

---

## 3. 4-bit ALU

The ALU currently supports:

| Opcode | Operation |
|---|---|
| `000` | AND |
| `001` | OR |
| `010` | XOR |
| `011` | ADD |
| `100` | NOT A |
| `101` | unused |
| `110` | unused |
| `111` | unused |

The ALU also produces three flags:

- `Z` — Zero: the result is `0000`
- `C` — Carry: an arithmetic carry leaves the 4-bit result
- `N` — Negative/sign bit: the most significant result bit is `1`

`alu_hw.py` uses NAND-based multiplexers to select the active ALU output from the opcode instead of using Python control flow for the simulated hardware-selection path.

Conceptually:

```text
AND ───┐
OR  ───┤
XOR ───┤
ADD ───┤──> MUX ──> RESULT
NOT ───┘
          ^
        opcode
```

---

## 4. Memory and registers

The project then moves from combinational logic to state.

A simplified D flip-flop model represents one stored bit.

A 4-bit register combines four of these storage elements:

```text
D3 D2 D1 D0
 |  |  |  |
 FF FF FF FF
 |  |  |  |
Q3 Q2 Q1 Q0
```

A register captures its input on a simulated clock edge.

The important distinction is:

```text
ALU      = computes the current result
Register = remembers a captured result
```

Example:

```text
ALU = 1101
REGISTER = 0000

CLOCK ↑

REGISTER = 1101
```

If the ALU later changes, the register keeps `1101` until another clock edge captures a new value.

---

## 5. ALU → Register cycle

`cpu_cycle.py` connects computation and state.

The machine can:

```text
calculate
   ↓
capture result
   ↓
reuse stored result
   ↓
calculate again
```

Example:

```text
3 + 10 = 13
CLOCK
REGISTER = 13

1 + 1 = 2
REGISTER still = 13

CLOCK
REGISTER = 2

REGISTER + 3 = 5
CLOCK
REGISTER = 5
```

This is the first CPU-style state cycle in the project.

---

## 6. Accumulator

`accumulator.py` introduces an accumulator register.

The accumulator is a register used as the CPU's main working value:

```text
ACC ──> ALU ──> ACC
```

This allows operations such as:

```text
LOAD 3
ADD 10
ADD 1
ADD 1
```

producing:

```text
ACC = 3
ACC = 13
ACC = 14
ACC = 15
```

The current `LOAD` path is intentionally simplified. A later hardware-control layer will choose between ALU output and externally loaded data.

---

## 7. Programs

`program.py` represents a program as data rather than as direct Python function calls.

Example:

```python
program = [
    ("LOAD", 3),
    ("ADD", 10),
    ("ADD", 1),
    ("ADD", 1),
]
```

This is an important transition:

```text
program
   ↓
instruction
   ↓
decode
   ↓
CPU
```

The instructions are still symbolic at this stage. They are not machine code yet.

---

## 8. Program Counter

`program_counter.py` adds a 4-bit Program Counter (`PC`).

The PC stores the address of the next instruction:

```text
PC = 0 -> instruction 0
PC = 1 -> instruction 1
PC = 2 -> instruction 2
```

After a normal instruction:

```text
PC = PC + 1
```

Because the PC is currently 4 bits wide:

```text
1111 + 1 = 0000
```

with a carry out.

The accumulator and Program Counter now have distinct roles:

```text
ACC = working calculation state
PC  = current program position
```

---

## 9. Fetch / Execute cycle

`machine.py` combines the Program Counter, program, accumulator and execution logic.

The current cycle is:

```text
1. PC contains an address
2. FETCH reads the instruction at that address
3. EXECUTE performs the instruction
4. ACC changes if required
5. PC increments
6. Repeat
```

Example:

```text
PC=0000
FETCH: LOAD 3
ACC=0011
NEXT PC=0001

PC=0001
FETCH: ADD 10
ACC=1101
NEXT PC=0010
```

Conceptually:

```text
          ┌──────────────┐
          │   PROGRAM    │
PC ──────>│   address    │
          └──────┬───────┘
                 │
              FETCH
                 │
            instruction
                 │
              EXECUTE
                 │
          ┌──────v───────┐
          │   ALU / ACC  │
          └──────────────┘
                 │
             PC = PC + 1
```

At this point the project has its first real fetch/execute loop.

---

## Current limitation

There is still an important abstraction layer left to remove.

The CPU currently receives instructions such as:

```text
ADD 10
```

and Python still helps decode the text operation.

A real CPU receives bits.

The next target is something conceptually like:

```text
0011 1010
^^^^ ^^^^
 ADD   10
```

The exact instruction format will be designed as part of the project.

---

## Roadmap

### Completed

- [x] NAND primitive
- [x] NOT / AND / OR / XOR
- [x] Half-adder
- [x] Full-adder
- [x] 4-bit ripple-carry adder
- [x] 4-bit ALU
- [x] NAND-based multiplexers
- [x] Z / C / N flags
- [x] Clocked 4-bit register
- [x] ALU → register cycle
- [x] Accumulator
- [x] Sequential symbolic programs
- [x] 4-bit Program Counter
- [x] Fetch / execute cycle

### Next

- [ ] Define the instruction encoding
- [ ] Replace symbolic instructions with machine code
- [ ] Build instruction decoding
- [ ] Add explicit HALT/control instructions
- [ ] Add RAM
- [ ] Add load/store operations
- [ ] Add branching/jumps
- [ ] Expand the CPU architecture
- [ ] Build an assembler
- [ ] Explore operating-system concepts
- [ ] Continue upward toward networking

---

## Project files

```text
gates.py            NAND, derived gates and binary adders
alu.py              4-bit ALU operations and flags
alu_hw.py           NAND-based multiplexers and hardware-selected ALU
memory.py           D flip-flop model and 4-bit register
cpu_cycle.py        ALU-to-register CPU-style cycles
accumulator.py      accumulator-based CPU model
program.py          sequential symbolic programs
program_counter.py  4-bit Program Counter
machine.py          fetch / execute machine loop
```

---

## Philosophy

The purpose of this project is not simply to emulate a CPU with Python.

The goal is to understand **why each component exists**, how it works, and how increasingly complex computer behavior emerges from simple binary logic.

Each layer is introduced only after the previous one is understandable:

```text
logic
  ↓
arithmetic
  ↓
state
  ↓
control
  ↓
program execution
```

The long-term goal is to keep climbing that stack until the path from **NAND to Network** is understandable end to end.
