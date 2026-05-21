# signac Setup on Perlmutter

## Installation

Install via conda environment (included in environment.yml):

```bash
module load python
pip install signac==2.3.0 signac-flow==0.28.0
```

## Verification

```bash
python -c "import signac; print(signac.__version__)"
```

Expected: 2.3.0

## See Also

- Section 1 examples: `01-signac/`
- Official docs: https://docs.signac.io/
