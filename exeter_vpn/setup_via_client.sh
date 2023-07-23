#!/bin/bash

# Configure the VIA VPN software
# Turns off BASH history (if you're copy pasting!)
# Prevents plaintext passwords being visible
set +o history

# Start the server?
sudo via-vpn-srv

# Start a VIA session
via-cli session start --keypass <Password>
# via-cli session stop --force # <- If session needs ending

# Download the profile from Exeter's gateway by logging in
via-cli profile load \
    --gateway remote.exeter.ac.uk \
    --username USERNAME \
    --userpass PASSWORD

# TODO: Find way to obfuscate password (--userpassfile ???)

# Write Exeter's certificate to disk and import
cat <<EOF > exeter.cert
-----BEGIN CERTIFICATE-----
You have to go and download this, Exeter probably won't be happy me giving this out!
-----END CERTIFICATE-----
EOF

via-cli cert import --user --keypass <Password> --CA exeter.cert

# Certificate 'exeter.cert' was successfully imported.
# Alias:   U.d7a7a0fb5d7e2731d771e9484ebcdef71d5f0c3e0a2948782bc83ee0ea699ef4
# Subject: AAA Certificate Services
# Issuer:  AAA Certificate Services
# FromDate:01 Jan 2004
# ExpDate: 31 Dec 2028
# Type:    CA
# Sign algorithm: RSA
# Hash algorithm: SHA1

# Turn BASH history back on
set -o history

# Connect to VPN and check we're connected
via-cli vpn connect
# via-cli vpn disconnect # <- disconnect
via-cli vpn status
