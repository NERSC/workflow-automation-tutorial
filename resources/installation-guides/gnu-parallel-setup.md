# GNU Parallel Setup on Perlmutter

## Installation

GNU Parallel is available via module on Perlmutter:

```bash
module load parallel
parallel --version
```

No additional installation needed.

## Verification

```bash
seq 1 4 | parallel echo "Test {}"
```

Expected output: "Test 1", "Test 2", "Test 3", "Test 4"

## See Also

- Section 0 examples: `00-gnu-parallel/`
- Official docs: https://www.gnu.org/software/parallel/
