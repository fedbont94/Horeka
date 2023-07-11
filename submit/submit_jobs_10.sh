#!/bin/bash
python3 submit_jobs_10.py
# sbatch -p cpuonly -A hk-project-radiohfi --job-name=sub10 ./submit_jobs_10.sh