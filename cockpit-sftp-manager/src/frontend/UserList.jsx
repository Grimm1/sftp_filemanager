import React from 'react';
import { Table, TableHeader, TableBody, TableVariant } from '@patternfly/react-table';
import { Button } from '@patternfly/react-core';
import cockpit from 'cockpit';

const UserList = ({ users }) => {
  const columns = ['Username', 'Chroot Path', 'Last Login', 'Status', 'Actions'];
  
  const rows = users.map(user => [
    user.username,
    user.chroot_path,
    user.last_login || 'Never',
    user.enabled ? 'Enabled' : 'Disabled',
    <div key={user.username}>
      <Button variant="secondary" onClick={() => handleAction(user.username, 'disable')}>
        {user.enabled ? 'Disable' : 'Enable'}
      </Button>
      <Button variant="danger" onClick={() => handleAction(user.username, 'delete')}>
        Delete
      </Button>
      <Button variant="secondary" onClick={() => handleAction(user.username, 'regen')}>
        Regenerate Password
      </Button>
    </div>
  ]);

  const handleAction = (username, action) => {
    cockpit.spawn(["python3", "/usr/lib/cockpit/sftp-manager/sftp_manager.py", action, username])
      .then(() => window.location.reload())
      .catch(err => console.error(`Error ${action} user:`, err));
  };

  return (
    <Table caption="SFTP Users" variant={TableVariant.compact} cells={columns} rows={rows}>
      <TableHeader />
      <TableBody />
    </Table>
  );
};

export default UserList;