# Overview
This role was designed for integration with the Okta RADIUS Agent for Linux in order to get MFA for SSH.

## Prerequisites
1. Figure out which server will host your RADIUS Agent
2. Make sure firewalls, etc all traffic in
` sudo firewall-cmd --zone=public --add-port=1812/udp `
or whatever zone you use.
3. Other prereqs

## Architecture
Authentication Server: Okta SaaS tenant
RADIUS Server: Okta Radius Agent for Linux installed on a VM
Clients: All servers with pam_radius installed and configured to talk to the RADIUS server.

The agent is installed on a server (or potentially container if you want); and listens on port 1812.
The remote servers receive a PAM configuration that points them to the server with the Agent, which then calls Okta and authenticates the user. The configuration also contains a secret that is generated at the Authentication Server.


## SSH Access
Users authenticate into the server over SSH and are prompted for a password, which corresponds to their Okta account.
Once a valid password is entered, the user is prompted for a Time-Based One Time Password (TOTP).

Currently, the pam configuration is set to "sufficient", so it's not required and users can bypass with a password, which removes the benefit of MFA, making it an optional authentication approach. No bueno.

## sudo access
This Role includes a "sudo" file to update /etc/pam.d/sudo but does not copy the file over. 
> To do: Create true/false flags in the playbook and add "MFA Enable SUDO: true/false"; if true then copy, if false then don't

## Other Stuff
This solution creates a dependency on a bunch external, out-of-your-control services in order to support accessing your local VMs. That's a risk.

## Alternatives
Google Authenticator PAM; but everyone has to scan a QR code and that will create an individual entry for every VM - kind of a pain.
SSSD - requires an external domain of some kind.
Probably some other things.
