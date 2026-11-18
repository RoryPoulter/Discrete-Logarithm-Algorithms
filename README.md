# Discrete-Logarithm-Algorithms

![GitHub License](https://img.shields.io/github/license/RoryPoulter/Discrete-Logarithm-Algorithms?style=for-the-badge)
![GitHub Issues](https://img.shields.io/github/issues/RoryPoulter/Discrete-Logarithm-Algorithms?style=for-the-badge)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/RoryPoulter/Discrete-Logarithm-Algorithms/pylint.yml?style=for-the-badge&logo=Python&logoColor=ffffff)
![GitHub Release](https://img.shields.io/github/v/release/RoryPoulter/Discrete-Logarithm-Algorithms?include_prereleases&style=for-the-badge)



# Contents
- [Discrete-Logarithm-Algorithms](#discrete-logarithm-algorithms)
- [Contents](#contents)
  - [Background](#background)
    - [The Discrete Loagrithm Problem](#the-discrete-loagrithm-problem)
    - [Algorithms](#algorithms)
  - [Package Syntax](#package-syntax)
    - [Basic Algorithms](#basic-algorithms)
    - [`parallel_pohlig_hellman`](#parallel_pohlig_hellman)
    - [Utility Functions](#utility-functions)

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
* `g` (`int`) - The generator for the group $G$
* `h` (`int`) - The result of the equation $h = g^x \ mod \ p$
* `p` (`int`) - The prime base of the group $G$

**Returns**:
* `x` (`int`) - The exponent which solves the equation $h = g^x \ mod \ p$

### `parallel_pohlig_hellman`

Below is the syntax for the parallel implementation of the Pohlig-Hellman algorithm.

```py
x = parallel_pohlig_hellman(g, h, p, max_threads=8)
```

**Parameters**:
* `g` (`int`) - The generator for the group $G$.
* `h` (`int`) - The result of the equation $h = g^x \ mod \ p$.
* `p` (`int`) - The prime base of the group $G$.
* `max_threads` (`int`, *optional*) - The maximum number of threads allocated to the subgroups. Defaults to 4.

**Returns**:
* `x` (`int`) - The exponent which solves the equation $h = g^x \ mod \ p$

### Utility Functions
```py
valid: bool = verify(g, h, p, x)  # Verifies the discrete log found is correct
smooth: int = smoothness(n)  # Finds the smoothness of an integer n - the largest prime factor
```