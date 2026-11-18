# CHANGELOG

## v0.4.2 [18/11/2026]

**Optimisations for Pohlig-Hellman and BSGS.**
### Improvements
- Swapped `ThreadPoolExecutor` for `ProcessPoolExecutor` for better parallelisation in `parallel_pohlig_hellman`
- Add optional group order parameter `n_i` to `baby_step_giant_step`
### Bug Fixes
- Update `solve_ph_subgroup` to try group order of $n_i$ before resorting to $p-1$
### Other Changes
- Add test suite to `main.py` for serial and parallel PH comparison

## v0.4.1 [18/11/2026]

**Implementation of parallel Pohlig-Hellman algorithm.**
### Improvements
- Move shared code for Pohlig-Hellman implementations to `utils.py`
- Add documentation for `parallel_pohlig_hellman` and utility funcitons
### Other Changes
- Create `CHANGELOG.md`
- Add comments with prime smoothness to test cases
- Update `README.md` with badges and more intuitive group theory notation

[**Full Changelog**](https://github.com/RoryPoulter/Discrete-Logarithm-Algorithms/commits/v0.4.1)