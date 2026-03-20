# Workflow Tool Troubleshooting Guide

A comprehensive troubleshooting guide for common issues encountered when using GNU Parallel, signac, Maestro, Merlin, and AiiDA on HPC systems.

Each section includes symptom identification, diagnostic commands, and practical solutions.

---

## GNU Parallel Troubleshooting

### Problem: "parallel: command not found"

**Symptom:** Error when attempting to run parallel commands on Perlmutter

```
bash: parallel: command not found
```

**Diagnosis:**
```bash
which parallel
module avail parallel
```

**Solution:**

GNU Parallel is provided via module on Perlmutter. Load the module:

```bash
module load parallel
parallel --version
```

Verify installation succeeded:

```bash
echo "test" | parallel echo {}
```

### Problem: Output appears in wrong order or seems scrambled

**Symptom:** Results from parallel jobs print in random order, making it hard to understand which output came from which input

**Diagnosis:**
```bash
# Check if --linebuffer or --tagstring is in your command
parallel --help | grep -A2 "linebuffer\|tagstring"
```

**Solution:**

Use output ordering options to track which result corresponds to which input:

```bash
# Option 1: Tag each output with input value
seq 1 10 | parallel --tagstring "Task {}" echo "Processing {}"

# Option 2: Buffer lines to keep output together
seq 1 10 | parallel --linebuffer echo "Line {}" && echo "Done with {}"

# Option 3: Save to individual files (most reliable)
seq 1 10 | parallel "echo 'Result for {}' > result_{}.txt"
cat result_*.txt | sort
```

### Problem: Parallel not using all available cores

**Symptom:** Jobs run slower than expected even with -j flag set

**Diagnosis:**
```bash
# Check how many cores parallel detected
parallel --version | grep "spawning"
grep -c ^processor /proc/cpuinfo
parallel -j 0 --dry-run echo {} ::: {1..10}
```

**Solution:**

Explicitly set job slots to number of available cores:

```bash
# Use -j N to specify exactly N parallel jobs
parallel -j 8 echo "Job {}" ::: {1..100}

# Or use -j 0 to use all available cores
parallel -j 0 echo "Job {}" ::: {1..100}

# For SLURM-allocated nodes, match SLURM_CPUS_PER_TASK
parallel -j $SLURM_CPUS_PER_TASK command {} ::: input1 input2 input3
```

### Problem: Out of memory or "Cannot fork" error

**Symptom:** Error: Cannot fork: Resource temporarily unavailable

```
error: Cannot fork: Resource temporarily unavailable
error: Out of memory
```

**Diagnosis:**
```bash
# Check available memory
free -h
# Check ulimits
ulimit -a
# Check system load
top -b -n1 | head -20
```

**Solution:**

Reduce parallelization or increase memory per job:

```bash
# Reduce number of parallel jobs
parallel -j 2 command {} ::: input_list

# Increase memory request in SLURM
#SBATCH --mem=32GB
#SBATCH --cpus-per-task=8
parallel -j 8 memory_intensive_command {} ::: {1..100}
```

---

## signac Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'signac'"

**Symptom:** Python import fails when trying to use signac

```
ModuleNotFoundError: No module named 'signac'
```

**Diagnosis:**
```bash
python -c "import signac; print(signac.__version__)"
pip list | grep signac
which python
```

**Solution:**

Install signac with pip in correct Python environment:

```bash
module load python
pip install signac==2.3.0 signac-flow==0.28.0

# Verify installation
python -c "import signac; import signac_flow; print(signac.__version__)"
```

### Problem: "Incompatible file format" when opening project

**Symptom:** Error when opening existing signac project from different version

```
Incompatible file format. Run "signac migrate" to upgrade.
```

**Diagnosis:**
```bash
cd /path/to/project
signac find
```

**Solution:**

Migrate project to current signac format:

```bash
cd /path/to/project
signac migrate
# Verify migration succeeded
signac find | wc -l
```

### Problem: Job decorators not being recognized

**Symptom:** @flow.cmd decorator or @flow.operation not working, jobs don't execute

**Diagnosis:**
```bash
# Check project structure
ls -la
cat signacrc.json
# Try running manually
python -c "from flow import FlowProject; print(FlowProject)"
```

**Solution:**

Ensure project has correct structure and flow is imported:

```python
#!/usr/bin/env python
from signac import init_project
from signac_flow import FlowProject, cmd, flow

project = init_project('MyProject')

class MyFlow(FlowProject):
    pass

@MyFlow.operation
def my_operation(job):
    print(f"Running job {job.id}")
    # Your code here
```

Then execute:

```bash
python flow.py run
```

### Problem: Permission denied on workspace directories

**Symptom:** Error: Permission denied when accessing job workspace

```
PermissionError: [Errno 13] Permission denied: '/path/to/workspace/...'
```

**Diagnosis:**
```bash
# Check workspace permissions
ls -ld workspace
ls -l workspace/*/
# Check umask
umask
```

**Solution:**

Set proper umask and correct permissions:

```bash
# Before creating jobs, set permissive umask
umask 0002

# Fix existing permissions
chmod -R g+rwx workspace/
# Ensure group ownership is correct
chgrp -R $(id -g) workspace/

# Verify
ls -ld workspace
```

### Problem: "signac run" submits jobs but they don't execute

**Symptom:** Jobs appear in queue but status shows 'submitted' indefinitely

**Diagnosis:**
```bash
signac job-info
squeue -u $USER
# Check submission script
cat $(signac find | head -1)/signacrc.json
```

**Solution:**

Verify SLURM submission script is configured correctly:

```bash
# In signacrc.json, ensure scheduler configuration
cat signacrc.json
# If missing scheduler, add it
signac config set "flow.scheduler" "Slurm"

# Check job environment
signac job-info
```

---

## Maestro Troubleshooting

### Problem: "maestro: command not found"

**Symptom:** Command line interface not available

```
bash: maestro: command not found
```

**Diagnosis:**
```bash
which maestro
python -c "import maestrowf; print(maestrowf.__version__)"
pip list | grep maestro
```

**Solution:**

Install Maestro via pip:

```bash
module load python
pip install maestrowf==1.1.11
maestro --version
```

### Problem: YAML syntax error in specification file

**Symptom:** Error when parsing workflow specification

```
YAML parsing error: mapping values are not allowed in this context
```

**Diagnosis:**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('spec.yaml'))"
# Check indentation
cat -A spec.yaml | head -20
```

**Solution:**

Fix YAML formatting:

```yaml
# Correct: proper indentation
workflow:
  name: my_workflow
  steps:
    - name: step1
      command: echo "Hello"
    - name: step2
      command: echo "World"
      depends: [step1]

# Incorrect: inconsistent indentation
workflow:
  name: my_workflow
    steps:
      - name: step1
```

Verify fixed YAML:

```bash
maestro --dry-run spec.yaml
```

### Problem: Workflow hangs or appears to be stuck

**Symptom:** maestro status shows workflow running but no progress for extended time

**Diagnosis:**
```bash
# Check workflow status
maestro status
# Look for stuck tasks
maestro report -d $(maestro list | tail -1)
# Check system resources
squeue -u $USER
top -u $USER
```

**Solution:**

Investigate and restart:

```bash
# View detailed status
maestro status -v

# Kill workflow if truly stuck
maestro cancel -d $(maestro list | tail -1)

# Check for circular dependencies
maestro --dry-run spec.yaml

# Resubmit after fixing
maestro run spec.yaml
```

### Problem: "Node not found" or invalid batch parameters

**Symptom:** Error in Slurm batch block configuration

```
KeyError: Node not found
Error: Invalid partition name
```

**Diagnosis:**
```bash
# Check available partitions
sinfo
# Check account availability
sacctmgr show user $USER format=Account
```

**Solution:**

Use valid SLURM parameters in batch block:

```yaml
study:
  # ...
  batch:
    type: slurm
    host: perlmutter
    queue: regular
    nodes: 2
    ppn: 128
    walltime: "01:00:00"
    account: m1234   # Valid account for your project
```

### Problem: Output files not created in expected location

**Symptom:** Workflow completes but output directory is empty

**Diagnosis:**
```bash
# Check working directory
pwd
# Search for outputs
find . -name "*.txt" -o -name "*.dat" 2>/dev/null
# Check environment variables
echo $SCRATCH
```

**Solution:**

Explicitly specify output paths in workflow:

```yaml
study:
  description: "Ensure outputs are written"
  steps:
    - name: compute
      command: "python compute.py"
      output:
        directory: results/

    - name: save
      command: "cp results/* $SCRATCH/final_results/"
      depends: [compute]
```

---

## Merlin Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'merlin'"

**Symptom:** Cannot import merlin in Python scripts

```
ModuleNotFoundError: No module named 'merlin'
```

**Diagnosis:**
```bash
python -c "import merlin; print(merlin.__version__)"
pip list | grep merlin
which merlin
```

**Solution:**

Install Merlin with all dependencies:

```bash
module load python
pip install merlin[redis]==1.11.6

# Verify installation
merlin --version
python -c "from merlin.spec.specification import MerlinSpecification"
```

### Problem: Redis connection refused or not running

**Symptom:** Error when submitting workflow to Merlin

```
ConnectionRefusedError: Error 111 connecting to localhost:6379
redis.exceptions.ConnectionError: Error -2 connecting to redis-server:6379
```

**Diagnosis:**
```bash
# Check if Redis is running
redis-cli ping
# Check port availability
netstat -tlnp | grep 6379
# Check Redis logs
redis-cli info
```

**Solution:**

Start Redis server (if using local instance):

```bash
# Option 1: Start in current session
redis-server --port 6379 &

# Option 2: Start with NERSC-provided Redis module (if available)
module load redis
redis-server &

# Verify connection
redis-cli ping
# Should return: PONG

# Then submit workflow
merlin run spec.yaml
```

For production deployments, request Redis instance from NERSC.

### Problem: Workers not picking up tasks

**Symptom:** Tasks remain in queue but no workers execute them

```
merlin status
# Shows: pending=100, running=0, finished=0
```

**Diagnosis:**
```bash
# Check worker processes
merlin ps
# Check queue contents
redis-cli LLEN celery
# Check worker logs
tail -f merlin_worker.log
```

**Solution:**

Start Merlin workers and submit tasks:

```bash
# Terminal 1: Start worker(s)
merlin workers start spec.yaml --worker-name default --worker-threads 4

# Terminal 2: Submit workflow
merlin run spec.yaml

# Monitor progress
merlin status
```

For persistent workers on NERSC, submit worker job separately:

```bash
# Submit long-running worker job
sbatch worker_submission.sh

# Then submit workflow
merlin run spec.yaml
```

### Problem: "Study not found" or workflow specification error

**Symptom:** Merlin cannot locate study or parse specification

```
Error: Study 'my_study' not found
Error parsing workflow specification
```

**Diagnosis:**
```bash
# List available studies
merlin status
# Validate specification
merlin run spec.yaml --dry-run
# Check file syntax
python -c "import yaml; yaml.safe_load(open('spec.yaml'))"
```

**Solution:**

Ensure specification is valid and studies are defined:

```yaml
description: "Valid Merlin specification"

studies:
  - name: my_study
    description: "My first study"

    spec:
      parameters:
        x: [1, 2, 3]
        y: [4, 5, 6]

      steps:
        - name: setup
          command: "echo 'Setup'"

        - name: run
          command: "python analyze.py $(X) $(Y)"
          depends: [setup]
```

Verify:

```bash
merlin run spec.yaml --dry-run
```

### Problem: Permission denied when writing to NERSC filesystems

**Symptom:** Tasks fail with permission errors writing to $SCRATCH

```
PermissionError: [Errno 13] Permission denied
IOError: [Errno 13] Permission denied: '/global/cfs/cdirs/m1234/...'
```

**Diagnosis:**
```bash
# Check current user
whoami
# Check $SCRATCH ownership and permissions
ls -ld $SCRATCH
# Check file group
ls -l $SCRATCH/test_file.txt
```

**Solution:**

Configure proper NERSC environment in Merlin:

```yaml
spec:
  env:
    variables:
      # Use $SCRATCH for temporary workflow data
      WORKFLOW_DIR: $SCRATCH/my_workflow
      # Use CFS directory for long-term results (if available)
      RESULTS_DIR: $PSCRATCH/results

  steps:
    - name: write
      command: |
        mkdir -p $WORKFLOW_DIR
        python compute.py > $WORKFLOW_DIR/output.txt
```

---

## AiiDA Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'aiida'"

**Symptom:** Cannot import or run AiiDA

```
ModuleNotFoundError: No module named 'aiida'
```

**Diagnosis:**
```bash
python -c "import aiida; print(aiida.__version__)"
pip list | grep aiida
which verdi
```

**Solution:**

Install AiiDA with database support:

```bash
module load python
pip install aiida-core==2.4.0 aiida-core[postgres]

# Initialize AiiDA
verdi quicksetup

# Verify installation
verdi status
```

### Problem: PostgreSQL connection failed

**Symptom:** Error when starting AiiDA daemon

```
psycopg2.OperationalError: could not connect to server
Database 'aiida_db' does not exist
```

**Diagnosis:**
```bash
# Check PostgreSQL status
psql --version
# Try connecting
psql -h localhost -U postgres
# Check AiiDA config
cat ~/.aiida/config.json | grep -A5 postgresql
```

**Solution:**

Ensure PostgreSQL is running and AiiDA is configured:

```bash
# Start PostgreSQL (if not already running)
pg_ctl -D /path/to/postgres/data start

# Or, use NERSC-provided PostgreSQL service (if available)
module load postgresql

# Verify connection
psql -U postgres -c "SELECT 1"

# Reconfigure AiiDA
verdi quicksetup

# Check status
verdi status
```

### Problem: Daemon not starting or stuck in "stopped" state

**Symptom:** "verdi status" shows daemon as stopped despite start attempts

```
Daemon status: STOPPED
```

**Diagnosis:**
```bash
# Check daemon logs
verdi devel get-daemon-worker-log

# Check for stale processes
ps aux | grep -i aiida
ps aux | grep -i celery

# Check daemon config
cat ~/.aiida/config.json | grep daemon
```

**Solution:**

Clean up and restart daemon:

```bash
# Stop any stray processes
killall -9 celery python 2>/dev/null

# Clean daemon
verdi daemon stop

# Wait for cleanup
sleep 5

# Start fresh
verdi daemon start

# Verify
verdi status
```

### Problem: "Computer 'perlmutter' not found" or configuration error

**Symptom:** Workflow cannot find configured compute resource

```
InputValidationError: Computer 'perlmutter' does not exist
```

**Diagnosis:**
```bash
# List configured computers
verdi computer list

# Check if Perlmutter computer exists
verdi computer show perlmutter

# Check configuration
cat ~/.aiida/config.json | grep -A10 computers
```

**Solution:**

Configure Perlmutter as AiiDA compute resource:

```bash
# Add Perlmutter computer
verdi computer setup --label perlmutter \
  --hostname perlmutter.nersc.gov \
  --transport ssh \
  --scheduler slurm \
  --work-dir /pscratch/sd/username/aiida_work

# Test connection
verdi computer test perlmutter

# Verify
verdi computer list
```

### Problem: Workflow execution hangs or tasks don't complete

**Symptom:** Submitted workflow appears to run indefinitely

**Diagnosis:**
```bash
# Check workflow status
verdi process list -a

# Check specific process
verdi process show <process_id>

# Check logs
verdi process report <process_id>

# Check RabbitMQ status (if using distributed mode)
rabbitmq-diagnostics status
```

**Solution:**

Debug and resubmit:

```bash
# View process details and logs
verdi process report <process_id>

# Kill stuck process if needed
verdi process kill <process_id>

# Check for database locks
verdi daemon status

# Restart if needed
verdi daemon restart

# Check and fix workflow
python -c "from aiida import load_node; print(load_node(<process_id>))"
```

### Problem: Results not saved or data not persisted

**Symptom:** Workflow completes but output nodes are empty or missing

**Diagnosis:**
```bash
# List all nodes
verdi node list

# Check specific node
verdi node show <node_id>

# Check node outputs
verdi node repo dump <node_id>
```

**Solution:**

Ensure workflow saves results explicitly:

```python
from aiida import orm

# Create output nodes
output_data = orm.Dict(dict={'result': 42})
output_data.store()

# Return in workchain
return {'output': output_data}
```

Verify:

```bash
verdi node list
verdi node show <node_id>
verdi node repo dump <node_id>
```

### Problem: "Invalid input type" or node validation errors

**Symptom:** Workflow fails with validation error

```
ValueError: Invalid input type for socket 'x'
```

**Diagnosis:**
```bash
# Check node input ports
verdi process show <process_id> --inputs

# Validate inputs
python -c "from aiida import orm; print(orm.Int(5))"
```

**Solution:**

Use correct AiiDA data types:

```python
from aiida import orm

# Correct: use AiiDA types
input_int = orm.Int(42)
input_str = orm.Str("hello")
input_dict = orm.Dict(dict={'key': 'value'})

# Incorrect: native Python types
input_int = 42  # Wrong
input_str = "hello"  # Wrong
```

---

## Cross-Tool Issues

### Problem: Jobs failing due to insufficient disk space

**Symptom:** I/O errors, "No space left on device"

```
OSError: [Errno 28] No space left on device
IOError: [Errno 28] No space left on device
```

**Diagnosis:**
```bash
# Check filesystem usage
df -h $SCRATCH
du -sh $(pwd)/*

# Identify large files
find . -size +1G -type f
```

**Solution:**

Clean up and use appropriate filesystems:

```bash
# Remove unnecessary data
rm -rf old_runs/
rm *.log

# Use $SCRATCH for temporary data (it's larger)
cd $SCRATCH

# Monitor space usage
watch -n 60 'df -h $SCRATCH'
```

### Problem: Out of memory (OOM) errors

**Symptom:** Process killed or memory exhausted error

```
Killed: 9
MemoryError: Unable to allocate memory
```

**Diagnosis:**
```bash
# Check memory limits
ulimit -a
free -h

# Monitor during execution
watch -n 2 'free -h'
```

**Solution:**

Increase memory allocation or reduce memory usage:

```bash
# Increase SLURM memory request
#SBATCH --mem=64GB

# Or reduce task memory footprint
# - Process smaller chunks
# - Use streaming instead of loading entire file
# - Profile with memory tools

# For signac/Maestro/Merlin/AiiDA workflows:
# Reduce task parallelism to use less total memory
```

### Problem: Slurm integration errors across multiple tools

**Symptom:** Jobs not submitting or failing in queue

```
Error: Invalid account
Error: Partition not found
sbatch: error: QOS is not available
```

**Diagnosis:**
```bash
# Check available accounts
sacctmgr show user $USER format=Account

# List valid partitions
sinfo

# Check QOS limits
scontrol show qos

# Verify job submission syntax
sbatch --help | head -20
```

**Solution:**

Use correct SLURM parameters for your project:

```bash
# Find your valid account
sacctmgr show user $USER format=Account

# Use in workflow configuration
# GNU Parallel / Maestro / Merlin / AiiDA all need:
#SBATCH --account=m1234   # Your valid account
#SBATCH --partition=regular  # or gpu, debug
#SBATCH --qos=normal  # or batch, interactive

# Example for Maestro:
# Add to batch block: account: m1234

# Example for Merlin:
# In submission script: --account=m1234

# Example for AiiDA:
# In computer config: account_string: m1234
```

### Problem: Slow performance or inefficient scheduling

**Symptom:** Workflows run but take longer than expected

**Diagnosis:**
```bash
# Monitor execution
squeue -u $USER
top -u $USER

# Check system contention
uptime
w

# Profile workflow
time workflow_command
```

**Solution:**

Optimize workflow scheduling:

```bash
# 1. Avoid oversubscription
# Use -j N in GNU Parallel = number of cores
# Use nodes*ppn in Maestro batch block

# 2. Batch small tasks
# Instead of 10000 parallel jobs, group into 100 with 100 tasks each

# 3. Use appropriate partition
# debug: fast queue, limited time/nodes
# regular: production queue
# gpu: if your workflow uses GPUs

# 4. Profile and optimize
# Use perf, cProfile, or timing measurements
```

---

## Support and Further Help

If you encounter issues not covered here:

1. Check official documentation:
   - GNU Parallel: https://www.gnu.org/software/parallel/
   - signac: https://docs.signac.io/
   - Maestro: https://maestrowf.readthedocs.io/
   - Merlin: https://merlin.readthedocs.io/
   - AiiDA: https://aiida.readthedocs.io/

2. Search community forums:
   - AiiDA Discourse: https://aiida.discourse.group/
   - Merlin GitHub Issues: https://github.com/LLNL/merlin/issues
   - NERSC Help: https://docs.nersc.gov/

3. Contact NERSC User Support:
   - Email: help@nersc.gov
   - Phone: 1-510-486-8600

4. Review NERSC documentation:
   - Perlmutter Guide: https://docs.nersc.gov/systems/perlmutter/
   - File Systems: https://docs.nersc.gov/filesystems/
   - Job Scheduling: https://docs.nersc.gov/jobs/
