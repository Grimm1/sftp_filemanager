import React, { useState } from 'react';
import { Form, FormGroup, TextInput, Radio, Button, ActionGroup } from '@patternfly/react-core';
import cockpit from 'cockpit';

const UserForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    userType: 'new',
    passwordType: 'auto',
    password: '',
    chrootType: 'home',
    customPath: '',
    writableSubdir: false
  });

  const handleSubmit = () => {
    cockpit.spawn([
      "python3", "/usr/lib/cockpit/sftp-manager/sftp_manager.py", "create",
      JSON.stringify(formData)
    ])
      .then(() => window.location.reload())
      .catch(err => console.error("Error creating user:", err));
  };

  return (
    <Form>
      <FormGroup label="User Type" isRequired>
        <Radio
          isChecked={formData.userType === 'new'}
          name="userType"
          onChange={() => setFormData({ ...formData, userType: 'new' })}
          label="New User"
          id="new-user"
        />
        <Radio
          isChecked={formData.userType === 'existing'}
          name="userType"
          onChange={() => setFormData({ ...formData, userType: 'existing' })}
          label="Existing User"
          id="existing-user"
        />
      </FormGroup>
      <FormGroup label="Username" isRequired>
        <TextInput
          value={formData.username}
          onChange={value => setFormData({ ...formData, username: value })}
          id="username"
        />
      </FormGroup>
      <FormGroup label="Password">
        <Radio
          isChecked={formData.passwordType === 'auto'}
          name="passwordType"
          onChange={() => setFormData({ ...formData, passwordType: 'auto' })}
          label="Auto-generate"
          id="auto-password"
        />
        <Radio
          isChecked={formData.passwordType === 'manual'}
          name="passwordType"
          onChange={() => setFormData({ ...formData, passwordType: 'manual' })}
          label="Manual"
          id="manual-password"
        />
        {formData.passwordType === 'manual' && (
          <TextInput
            type="password"
            value={formData.password}
            onChange={value => setFormData({ ...formData, password: value })}
            id="password"
          />
        )}
      </FormGroup>
      <FormGroup label="Chroot Path">
        <Radio
          isChecked={formData.chrootType === 'home'}
          name="chrootType"
          onChange={() => setFormData({ ...formData, chrootType: 'home' })}
          label="Home Directory"
          id="home-chroot"
        />
        <Radio
          isChecked={formData.chrootType === 'custom'}
          name="chrootType"
          onChange={() => setFormData({ ...formData, chrootType: 'custom' })}
          label="Custom Path"
          id="custom-chroot"
        />
        {formData.chrootType === 'custom' && (
          <TextInput
            value={formData.customPath}
            onChange={value => setFormData({ ...formData, customPath: value })}
            id="custom-path"
          />
        )}
      </FormGroup>
      <FormGroup label="Writable Subdirectory">
        <Radio
          isChecked={formData.writableSubdir}
          name="writableSubdir"
          onChange={() => setFormData({ ...formData, writableSubdir: true })}
          label="Create writable 'upload' subdirectory"
          id="writable-subdir"
        />
      </FormGroup>
      <ActionGroup>
        <Button variant="primary" onClick={handleSubmit}>Submit</Button>
      </ActionGroup>
    </Form>
  );
};

export default UserForm;