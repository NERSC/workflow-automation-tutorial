#!/bin/bash
#SBATCH --job-name=parallel-demo
#SBATCH --nodes=1
#SBATCH --constraint=cpu
#SBATCH --qos=regular
#SBATCH --time=00:30:00
#SBATCH --account=<your_account>  # REPLACE with your NERSC account
#SBATCH --output=slurm-%j.out

# Slurm Integration Example for GNU Parallel on Perlmutter
# Demonstrates: batch submission, automatic core detection, fault tolerance

# Make sure process script is executable
chmod +x process_task.sh

echo "============================================"
echo "GNU Parallel + Slurm Integration Demo"
echo "============================================"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURMD_NODENAME"
echo "Nodes allocated: $SLURM_JOB_NUM_NODES"
echo "Cores per node: $SLURM_CPUS_ON_NODE"
echo "Working directory: $(pwd)"
echo "Task list: task_list.txt"
echo "Total tasks: $(wc -l < task_list.txt)"
echo "============================================"
echo ""

# Run GNU Parallel with:
# - Full core utilization ($SLURM_CPUS_ON_NODE = 128 on Perlmutter CPU nodes)
# - Job logging (--joblog tracks completion)
# - Fault tolerance (--resume-failed retries failures on resubmission)
# - 0.2 second delay between spawns (reduces Slurm controller load)
parallel \
  -j $SLURM_CPUS_ON_NODE \
  --joblog parallel_job.log \
  --resume-failed \
  --delay 0.2 \
  < task_list.txt

echo ""
echo "============================================"
echo "All tasks complete!"
echo "Job log: parallel_job.log"
echo "============================================"
echo ""
echo "To check for failures:"
echo "  grep -v '^Seq' parallel_job.log | awk '\$7 != 0'"
echo ""
echo "To retry failed tasks:"
echo "  sbatch submit_parallel_job.sh"
echo "  (--resume-failed automatically skips successful tasks)"
