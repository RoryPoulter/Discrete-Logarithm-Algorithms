# Discrete-Logarithm-Algorithms

# Contents
- [Discrete-Logarithm-Algorithms](#discrete-logarithm-algorithms)
- [Contents](#contents)
  - [Background](#background)
    - [The Discrete Loagrithm Problem](#the-discrete-loagrithm-problem)
    - [Algorithms](#algorithms)
  - [Package Syntax](#package-syntax)
    - [Basic Algorithms](#basic-algorithms)

Implementing discrete logarithm algorithms and comparing run-times on different inputs. The algorithms are configured for the multiplicative group of integers modulo $p$, written as $(\mathbb{Z}/p\mathbb{Z})^{\times}$

The package `discrete_log` contains implementations of the following discrete logarithm algorithms:
* Baby-step giant-step
* Pohlig-Hellman
* Pollard's Kangaroo
* Pollard's Rho

## Background
### The Discrete Loagrithm Problem
The Discrete Logarithm Problem (DLP) is the process of solving equations for $x$ in the following form:

$h = g^x \mod p$

where $p$ is a prime and $g$ is a generator of a group $G = (\mathbb{Z}/p\mathbb{Z})^{\times}$.

They are the basis of Diffie-Hellman Key Exchange and the ElGamal Encryption System. 

### Algorithms

There are currently no known efficient (polynomial time) algorithms for solving the equations for generic groups, especially on classical (non-quantum) computers.

The most commonly used algorithms are:
* Shank's Baby-step Giant-step
* Pollard's Rho
* Pollard's Kangaroo
* Pohlig-Hellman
* Index Calculus
* Number Field Sieve
* Function Field Sieve


## Package Syntax
### Basic Algorithms
Below is the syntax for the functions `baby_step_giant_step`, `pohlig_hellman`, `pollards_rho`, and `pollards_kangaroo`:

```py
x = func(g, h, p)
```

**Parameters**:
* `g` (`int`) - The generator for the group $GF(p)$
* `h` (`int`) - The result of the equation $h = g^x \ mod \ p$
* `p` (`int`) - The prime base of the group $GF(p)$

**Returns**:
* `x` (`int`) - The exponent which solves the equation $h = g^x \ mod \ p$

