# Overview

This role was designed for integration with the Okta RADIUS Agent for Linux.
The agent is installed on a server (or potentially container if you want); and listens on port 1812.
The remote servers receive a PAM configuration that points them to the server with the Agent, which then calls Okta and authenticates the user.

# SSH Access
Users authenticate into the server over SSH and are prompted for a password, which corresponds to their Okta account.
Once a valid password is entered, the user is prompted for a Time-Based One Time Password (TOTP).

Currently, the pam configuration is set to "sufficient", so it's not required and users can bypass with a password, which removes the benefit of MFA, making it an optional authentication approach. No bueno.

# sudo 
This Role includes a "sudo" file to update /etc/pam.d/sudo but does not copy the file over. 
> To do: Create true/false flags in the playbook and add "MFA Enable SUDO: true/false"; if true then copy, if false then don't


