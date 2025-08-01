import subprocess
import os

def update_ssh_config(username, chroot_path):
    config_file = '/etc/ssh/sshd_config'
    match_block = f"""
Match User {username}
    ChrootDirectory {chroot_path}
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
"""

    # Backup config
    subprocess.run(['cp', config_file, f'{config_file}.bak'], check=True)

    # Remove existing Match block for user
    with open(config_file, 'r') as f:
        lines = f.readlines()
    with open(config_file, 'w') as f:
        skip = False
        for line in lines:
            if f"Match User {username}" in line:
                skip = True
            elif skip and line.strip() == '':
                skip = False
            elif not skip:
                f.write(line)

    # Append new Match block
    with open(config_file, 'a') as f:
        f.write(match_block)

    # Validate config
    try:
        subprocess.run(['sshd', '-t'], check=True)
    except subprocess.CalledProcessError:
        # Restore backup if validation fails
        subprocess.run(['mv', f'{config_file}.bak', config_file], check=True)
        raise ValueError("Invalid SSH configuration")

    # Restart SSH service
    try:
        subprocess.run(['systemctl', 'restart', 'sshd'], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(['systemctl', 'restart', 'ssh'], check=True)  # Fallback for some distros
