# MYQASM

MYQASM stands for either My Quantum Assembly Language or Mylet's QUantum Assembly Language, depending on how vein I'm feeling.

It is based on Chapter 7.2 of "Quantum Computing for Computer Scientists" by N. S. Yanofsky and M. A. Mannucci, and is my attempt at Programming Drill 7.2.1.

The reason this markdown document exists is to clarify for myself how things work.

## Specification

MYQASM calls are made from within python using the syntax:

``` python
[variable = ] MYQASM("expression")
```

where `expression` is an expression to be executed, and,
if a result is returned, it can be stored in variable.

This is inspired by how one generally calls SQL from another language.
This felt appropriate, since this is in a sense a declarative language.

### Initialization of a register

``` MYQASM
INITIALIZE name N
```

where name is the identifier of the register containing the following characters only [A-Z][a-z][0-9][-][_][.], and N is the number of qubits in the register.

or

``` MYQASM
INITIALIZE name N [array]
```

where array is an array of length N of 0s and 1s that the register is to be initialized as.

e.g.

``` MYQASM
INITIALIZE R 5 [01001]
```

Initializes 5 qubits in the state |01001>.

### Selecting a subregister

``` MYQASM
SELECT name1 name2 N1 N2
```

where name1 is the identifier to store the subregister in, name2 is the subregister to select from, N1 is the offset to start from, and N2 is the number of qubits.

Roughly equivalent python:

``` python
name1 = name2[N1:N2]
```

### Concatenating gates

``` MYQASM
U CONCAT U1 U2
```

U is the gate you get after doing U1 and U2.

### Tensoring gates

``` MYQASM
U TENSOR U1 U2
```

U is the gate you get by doing U1 and U2 in parallel.

### Inverse of gates

``` MYQASM
U INVERSE U1
```

U is the inverse of U1.

This is easy to calculate, as for any unitary matrix U, U times the adjoint of U is the identity (by definition).

So the inverse is the adjoint.

### Apply a gate

```MYQASM
APPLY U R
```

Apply gate U to register R.

### Measure a register

```MYQASM
MEASURE R
```

Measure the register R, and return the result (so can be stored in python).

CLEAR? for clearing all registers?

## Pre-defined gates

Hadamard: H

Identity: I1, I2, I3 etc.

Rotation by arbitrary multiples of Pi: R1 (= R pi), R0.5 (= R pi by 2) etc..

Controlled-Not: CNOT
