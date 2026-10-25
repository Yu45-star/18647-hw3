#!/bin/bash
#SBATCH --job-name=lorenz_spark
#SBATCH --account=see260003p
#SBATCH --partition=RM
#SBATCH --nodes=2
#SBATCH --time=01:00:00
#SBATCH --output=slurm_logs/spark_%j.out
#SBATCH --error=slurm_logs/spark_%j.err

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"

module load anaconda3/2024.10-1
module load spark

# Use Python instead of IPython as the driver.
unset PYSPARK_DRIVER_PYTHON
export PYSPARK_PYTHON="$(which python)"

# Start the Spark cluster on allocated nodes.
/opt/packages/spark/scripts/spark-cluster-init.sh &
sleep 15

MASTER="spark://$(hostname -s).ib.bridges2.psc.edu:7077"

echo "Job ID: $SLURM_JOB_ID"
echo "Master: $MASTER"
echo "Start: $(date)"

spark-submit \
    --master "$MASTER" \
    --conf spark.sql.shuffle.partitions=64 \
    part2/src/analyze.py \
    --input "$PROJECT/18647-hw3/part1/results/trajectory_*.csv" \
    --output "$PROJECT/18647-hw3/part2/results/all_statistics"

echo "Finished: $(date)"
