# GNU Parallel Setup on Perlmutter

## Installation

GNU Parallel is pre-installed on Perlmutter — no module load or user installation required. It is available directly in `$PATH`:

```bash
parallel --version
```

## Verification

```bash
seq 1 4 | parallel echo "Test {}"
```

Expected output: "Test 1", "Test 2", "Test 3", "Test 4"

## See Also

- Section 0 examples: `00-gnu-parallel/`
- Official docs: https://www.gnu.org/software/parallel/
