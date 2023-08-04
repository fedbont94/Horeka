#!/bin/bash
python3 submit_jobs.py
# sbatch -p cpuonly -A hk-project-radiohfi --job-name=sub8 ./submit_jobs.sh