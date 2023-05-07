
# `scripts/`

This directory contains all scripts utilized in this repository. Please try and organize them by task into the existing subdirectories.

### Directories
- `data_backup`: scripts for backing up data
- `data_prep`: scripts that prepare data for other parts of the pipelin
- `data_processing`: scripts that process and analyze data

### Scripts
- `monthly_master_script.sh`: bash script that runs the entire top-FIBers pipeline from start to finish — triggered via cronjob each month (see `crontab.bak` for details