
#!/bin/bash
#SBATCH --job-name=lorenz
#SBATCH --account=see260003p
#SBATCH --partition=RM-shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --array=0-9%5
#SBATCH --output=slurm_logs/%A_%a.out
#SBATCH --error=slurm_logs/%A_%a.err

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"

module load anaconda3/2024.10-1
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate /ocean/projects/see260003p/yzeng13/lorenz_hw3_env

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

echo "Job: $SLURM_JOB_ID, Task: $SLURM_ARRAY_TASK_ID"
echo "Node: $(hostname)"
echo "Python: $(which python)"

python part1/src/generate_trajectory.py \
    --id "$SLURM_ARRAY_TASK_ID" \
    --output-dir part1/results
