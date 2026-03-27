#!/bin/bash
#
# submit.sh - Wrapper for submitting GNU Parallel batch jobs with optional SLURM reservation support
#
# Usage:
#   For training events:
#     export NERSC_TRAINING_RESERVATION=<reservation_name>
#     ./submit.sh
#
#   For regular usage:
#     ./submit.sh
#

# Check if NERSC_TRAINING_RESERVATION is set and non-empty
if [ -n "${NERSC_TRAINING_RESERVATION}" ]; then
    # Validate reservation name: only alphanumeric, underscores, and hyphens allowed
    if [[ "${NERSC_TRAINING_RESERVATION}" =~ [^a-zA-Z0-9_-] ]]; then
        echo "ERROR: Invalid reservation name. Only letters, digits, underscores, and hyphens are allowed."
        exit 1
    fi

    # Training event mode: add reservation and training account
    echo "=================================================="
    echo "Training event mode detected"
    echo "Reservation: ${NERSC_TRAINING_RESERVATION}"
    echo "Account: ntrain4"
    echo "=================================================="

    SBATCH_CMD="sbatch --reservation=${NERSC_TRAINING_RESERVATION} --account=ntrain4 submit_parallel_job.sh"
else
    # Regular submission mode: no additional flags
    echo "=================================================="
    echo "Regular submission mode"
    echo "Note: Account must be specified in submit_parallel_job.sh"
    echo "=================================================="

    SBATCH_CMD="sbatch submit_parallel_job.sh"
fi

# Print the exact command that will be executed
echo ""
echo "Executing: ${SBATCH_CMD}"
echo ""

# Execute sbatch command and propagate exit code
${SBATCH_CMD}
exit $?
