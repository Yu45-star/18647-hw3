
#!/bin/bash
#SBATCH --job-name=lorenz_batch
#SBATCH --account=see260003p
#SBATCH --partition=RM-shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --array=0-99%10
#SBATCH --output=slurm_logs/batch_%A_%a.out
#SBATCH --error=slurm_logs/batch_%A_%a.err

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"

module load anaconda3/2024.10-1
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate /ocean/projects/see260003p/yzeng13/lorenz_hw3_env

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

python part1/src/generate_batch.py \
    --batch-id "$SLURM_ARRAY_TASK_ID" \
    --batch-size 100 \
    --output-dir part1/results
