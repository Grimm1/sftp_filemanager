#!/usr/bin/env python3
import subprocess
import json
import os
import pwd
import crypt
import random
import string
import datetime
from ssh_config import update_ssh_config
from logger import log_action

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def create_user(data):
    username = data['username']
    user_type = data['userType']
    password = generate_password() if data['passwordType'] == 'auto' else data['password']
    chroot_path = f"/home/{username}" if data['chrootType'] == 'home' else data['customPath']
    writable_subdir = data['writableSubdir']

    try:
        # Validate inputs
        if not username.isalnum():
            raise ValueError("Invalid username")
        if data['chrootType'] == 'custom' and not os.path.isabs(chroot_path):
            raise ValueError("Invalid chroot path")

        if user_type == 'new':
            subprocess.run(['useradd', '-m', '-s', '/bin/false', username], check=True)
        else:
            try:
                pwd.getpwnam(username)
            except KeyError:
                raise ValueError("User does not exist")

        # Set password
        if password:
            encrypted_pass = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
            subprocess.run(['usermod', '-p', encrypted_pass, username], check=True)

        # Create chroot directory
        os.makedirs(chroot_path, exist_ok=True)
        os.chown(chroot_path, 0, 0)  # Root ownership
        os.chmod(chroot_path, 0o755)  # Read-only for root

        if writable_subdir:
            upload_path = os.path.join(chroot_path, 'upload')
            os.makedirs(upload_path, exist_ok=True)
            user_info = pwd.getpwnam(username)
            os.chown(upload_path, user_info.pw_uid, user_info.pw_gid)
            os.chmod(upload_path, 0o775)

        # Update SSH config
        update_ssh_config(username, chroot_path)

        # Log action
        log_action(username, password if data['passwordType'] == 'auto' else None, chroot_path, user_type)

        return {"status": "success", "password": password if data['passwordType'] == 'auto' else None}

    except Exception as e:
        log_action(username, None, chroot_path, "error", str(e))
        raise

def list_users():
    users = []
    with open('/etc/passwd', 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            username = parts[0]
            shell = parts[6]
            if shell == '/bin/false':  # Likely SFTP user
                try:
                    user_info = pwd.getpwnam(username)
                    last_login = get_last_login(username)
                    users.append({
                        'username': username,
                        'chroot_path': get_chroot_path(username),
                        'last_login': last_login,
                        'enabled': True  # Placeholder, extend for actual status
                    })
                except KeyError:
                    continue
    return users

def get_chroot_path(username):
    with open('/etc/ssh/sshd_config', 'r') as f:
        for line in f:
            if f"Match User {username}" in line:
                next_line = f.readline()
                if 'ChrootDirectory' in next_line:
                    return next_line.split()[1]
    return ''

def get_last_login(username):
    try:
        result = subprocess.run(['last', '-1', username], capture_output=True, text=True)
        return result.stdout.strip().split('\n')[0]
    except:
        return ''

def disable_user(username):
    subprocess.run(['usermod', '-L', username], check=True)
    log_action(username, None, None, "disable")

def delete_user(username):
    subprocess.run(['userdel', '-r', username], check=True)
    log_action(username, None, None, "delete")

def regenerate_password(username):
    password = generate_password()
    encrypted_pass = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
    subprocess.run(['usermod', '-p', encrypted_pass, username], check=True)
    log_action(username, password, None, "regen")
    return {"password": password}

if __name__ == '__main__':
    import sys
    action = sys.argv[1]
    
    if action == 'create':
        data = json.loads(sys.argv[2])
        result = create_user(data)
        print(json.dumps(result))
    elif action == 'list':
        print(json.dumps(list_users()))
    elif action == 'disable':
        disable_user(sys.argv[2])
    elif action == 'delete':
        delete_user(sys.argv[2])
    elif action == 'regen':
        result = regenerate_password(sys.argv[2])
        print(json.dumps(result))