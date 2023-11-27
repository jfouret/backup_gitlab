# Automated GitLab Backup Script

This Python script automates the backup of projects in a GitLab instance. It preserves the hierarchical structure of groups and projects, mirroring it in a local directory tree.

## Requirements

- Python 3.x
- GitLab server with API access
- `python-gitlab` and `GitPython` libraries (install with `pip install python-gitlab GitPython`)

## Usage

Run the script with Python:

```bash
python gitLab_backup.py --gitlab-url https://gitlab.example.com --access-token your_access_token --backup-path /path/to/backup
```
