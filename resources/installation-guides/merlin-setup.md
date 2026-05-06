# Merlin Setup on Perlmutter

## Installation

Merlin and its Python dependencies (`celery`, `redis` Python client) are included in the
`wf-seminar` conda environment:

```bash
module load python
conda activate wf-seminar
```

Or install directly via pip:

```bash
module load python
pip install merlin==1.13.0 'celery>=5.0,<6.0' 'redis>=6.0,<7.0'
```

## Configuration

Generate the default Merlin configuration file at `~/.merlin/app.yaml`:

```bash
merlin config
```

This creates a template with placeholder broker settings. Update the `broker` and
`results_backend` sections to point at a running Redis instance — see
[Redis broker setup](merlin-redis-setup.md).

## Verification

Check that the Merlin package installed correctly (no Redis required):

```bash
merlin --version
```

Expected: 1.13.0

Once Redis is configured, verify full broker connectivity:

```bash
merlin info
```

## See Also

- Redis broker setup (required to run workflows): `resources/installation-guides/merlin-redis-setup.md`
- Section 3 examples: `03-merlin/`
- Official docs: https://merlin.readthedocs.io/
