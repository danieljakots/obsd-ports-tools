#!/bin/sh

# Run all the list script and send a report

echo "# Broken ports (on amd64)"
sh list-broken-ports.sh
echo "--------------------------------------------------------------------"
echo "# Unhooked ports"
sh list-unhooked-ports.sh
echo "--------------------------------------------------------------------"
echo "# Unhooked py3 flavor"
sh list-unhooked-py3-ports.sh

