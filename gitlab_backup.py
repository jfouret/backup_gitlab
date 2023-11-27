import os
import sys
import git
import logging
import argparse
from gitlab import Gitlab

# Configure logging
logging.basicConfig(filename='gitlab_backup.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Set up the argument parser
parser = argparse.ArgumentParser(description='Automated GitLab Backup Script using SSH')
parser.add_argument('--gitlab-url', required=True, help='URL of your GitLab instance')
parser.add_argument('--access-token', required=True, help='Your GitLab personal access token')
parser.add_argument('--backup-path', required=True, help='Local path where backups will be stored')
parser.add_argument('--prefix', default='_', help='Prefix for group directories')

# Parse arguments
args = parser.parse_args()

# Initialize GitLab
gl = Gitlab(args.gitlab_url, private_token=args.access_token)

def backup_group(group, parent_dir):
    group_dir = os.path.join(parent_dir, args.prefix + group.name)
    os.makedirs(group_dir, exist_ok=True)
    
    # Backup projects in the group
    for project in group.projects.list(all=True):
        project_dir = os.path.join(group_dir, project.name)
        git_url = project.ssh_url_to_repo
        try:
            if os.path.exists(project_dir):
                repo = git.Repo(project_dir)
                repo.remote('origin').pull()
            else:
                git.Repo.clone_from(git_url, project_dir)
            logging.info(f'Successfully backed up project: {project.name}')
        except Exception as e:
            logging.error(f'Error backing up project {project.name}: {e}')
    # Backup immediate subgroups only (depth of 1)
    for subgroup in group.subgroups.list(all=True):
        backup_subgroup = gl.groups.get(subgroup.id)
        backup_group(backup_subgroup, group_dir)

def main():
    try:
        os.makedirs(args.backup_path, exist_ok=True)
        root_groups = gl.groups.list(all=True, top_level_only=True)
        for group in root_groups:
            backup_group(group, args.backup_path)
    except Exception as e:
        logging.error(f'Failed to complete backup: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
