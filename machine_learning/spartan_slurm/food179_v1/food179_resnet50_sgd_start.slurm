#!/bin/bash
# Created by the University of Melbourne job script generator for SLURM
# Sat Mar 02 2019 00:19:42 GMT+1100 (Australian Eastern Daylight Time)
# Multithreaded (SMP) job: must run on one node and the cloud partition
#SBATCH --nodes 1
#SBATCH --partition gpgpu
#SBATCH --gres=gpu:p100:4

# The name of the job:
#SBATCH --job-name="food179"

# The project ID which this job should run under:
#SBATCH --account="punim0784"

# Maximum number of tasks/CPU cores used by the job:
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12

# The amount of memory in megabytes per process in the job:
#SBATCH --mem=64G

# Send yourself an email when the job:
#SBATCH --mail-type=FAIL
# begins
#SBATCH --mail-type=BEGIN
# ends successfully
#SBATCH --mail-type=END

# Use this email address:
#SBATCH --mail-user=hanxunh@student.unimelb.edu.au

# The maximum running time of the job in days-hours:mins:sec
#SBATCH --time 23:59:00

# check that the script is launched with sbatch
if [ "x$SLURM_JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with sbatch"
   exit 1
fi


# Run the job from this directory:
cd /data/cephfs/punim0784/COMP90024-2019S1-Team7/machine_learning

# The modules to load:
module load Python/3.5.2-intel-2017.u2-GCC-5.4.0-CUDA9
nvidia-smi

python3 -u coconut_train.py --cuda  \
                            --start_from_begining   \
                            --train_batch_size 360  \
                            --test_batch_size 800   \
                            --num_epochs 400        \
                            --train_data_dir /data/cephfs/punim0784/comp90024_p2_food_179 \
                            --train_optimizer sgd   \
                            --model_type food179    \
                            --model_arc resnet50    \
                            --model_checkpoint_path checkpoints/food179_resnet50_sgd.pth \
                            >> logs/food179_resnet50_sgd.log
