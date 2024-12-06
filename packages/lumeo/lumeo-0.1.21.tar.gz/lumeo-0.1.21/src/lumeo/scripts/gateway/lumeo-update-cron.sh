#!/bin/bash

set -eo pipefail

wget -q https://assets.lumeo.com/lumeod/lumeo-gateway-update.sh -O /dev/shm/lumeo-gateway-update.sh

if [ -f /dev/shm/lumeo-gateway-update.sh ]; then
    sudo bash /dev/shm/lumeo-gateway-update.sh
    rm /dev/shm/lumeo-gateway-update.sh
fi
