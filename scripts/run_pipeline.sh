#!/bin/bash
#SBATCH --job-name=struct_mri
#SBATCH --output=logs/%j_struct_mri.out
#SBATCH --error=logs/%j_struct_mri.err
#SBATCH --time=02:00:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=4

# Structural MRI Processing Pipeline
# Workshop Example SLURM Script

echo "Starting structural MRI processing pipeline"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Date: $(date)"
echo ""

# Create logs directory if it doesn't exist
mkdir -p logs

# Load required modules (adjust for your HPC)
module purge
module load python/3.9

# Activate virtual environment
source ~/workshop/neuroimaging-workshop/venv/bin/activate

# Verify environment
echo "Python: $(which python)"
echo "Python version: $(python --version)"
echo ""

# Set up output directory
OUTPUT_DIR="${SLURM_SUBMIT_DIR}/outputs"
mkdir -p "${OUTPUT_DIR}"

# Run pipeline
echo "Running pipeline..."
python src/run_analysis.py

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Pipeline completed successfully!"
else
    echo ""
    echo "✗ Pipeline failed with error code $?"
    exit 1
fi

# Report results
echo ""
echo "Outputs saved to: ${OUTPUT_DIR}"
ls -lh "${OUTPUT_DIR}"

echo ""
echo "Job completed: $(date)"