import React from 'react';
import { Page, PageSection, PageSectionVariants } from '@patternfly/react-core';
import UserList from './UserList';
import UserForm from './UserForm';
import cockpit from 'cockpit';

const App = () => {
  const [users, setUsers] = React.useState([]);
  
  React.useEffect(() => {
    cockpit.spawn(["python3", "/usr/lib/cockpit/sftp-manager/sftp_manager.py", "list"])
      .then(data => setUsers(JSON.parse(data)))
      .catch(err => console.error("Error fetching users:", err));
  }, []);

  return (
    <Page>
      <PageSection variant={PageSectionVariants.light}>
        <UserForm />
        <UserList users={users} />
      </PageSection>
    </Page>
  );
};

export default App;