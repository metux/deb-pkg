#!/bin/bash

## generate a temporary gpp key for signing apt repo

set -e

HOSTNAME=`hostname -f`
USERNAME=`whoami`

gpg --full-gen-key --batch <(echo "Key-Type: 1"; \
                             echo "Key-Length: 4096"; \
                             echo "Subkey-Type: 1"; \
                             echo "Subkey-Length: 4096"; \
                             echo "Expire-Date: 0"; \
                             echo "Name-Real: Github build user"; \
                             echo "Name-Email: $USERNAME@$HOSTNAME"; \
                             echo "%no-protection"; )
