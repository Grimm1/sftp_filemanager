# Cockpit SFTP Manager Plugin

A Cockpit plugin for managing SFTP-only users with chroot restrictions.

## Prerequisites
- Cockpit >= 200
- Python 3
- npm
- Root access

## Installation

### From Source
1. Clone the repository:
   ```bash
   git clone https://grimm1/cockpit-sftp-manager.git
   cd cockpit-sftp-manager





Build and install:

make
sudo make install



Restart Cockpit:

systemctl restart cockpit

RPM Package (Fedora, CentOS)





Build RPM:

make package-rpm



Install:

sudo dnf install ./cockpit-sftp-manager-1.0.0-1.rpm

DEB Package (Ubuntu, Debian)





Build DEB:

make package-deb



Install:

sudo apt install ./cockpit-sftp-manager_1.0.0_all.deb

Usage





Access Cockpit at https://<server>:9090



Navigate to "SFTP User Manager" in the menu



Use the form to create or modify SFTP users



View and manage users in the table below

Logs





Actions are logged to /var/log/sftp_user_setup.log (root-only)

