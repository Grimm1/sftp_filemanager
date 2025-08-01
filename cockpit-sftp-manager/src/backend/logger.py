import os
import datetime

def log_action(username, password, chroot_path, action_type, error=None):
    log_file = '/var/log/sftp_user_setup.log'
    
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('')
        os.chown(log_file, 0, 0)
        os.chmod(log_file, 0o600)

    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"{timestamp} | {action_type} | User: {username}"
    if chroot_path:
        log_entry += f" | Chroot: {chroot_path}"
    if password:
        log_entry += f" | Password: {password}"
    if error:
        log_entry += f" | Error: {error}"
    log_entry += '\n'

    with open(log_file, 'a') as f:
        f.write(log_entry)
