#!/bin/sh

# This script blocks until the target machine pings.
# I'm using this after I rebooted a machine and I want to ssh it asap.

set -eu

usage() {
	echo "usage: ${0##*/} TARGET" 1>&2
	echo "usage: ${0##*/} TARGET TTL" 1>&2
	echo "\nBy default TTL is 30" 1>&2
	exit 1
}

notify() {
	/bin/echo -n -e "\a"
}

[ $# -gt 0 ] || usage

_target="$1"
_ttl="${2:-30}"

iter=0
while :;
do
	set +e
	ping -q -c2 "${_target}" > /dev/null
	res=$?
	set -e
	[ ${res} -eq 0 ] && break
	iter=$(( ${iter} + 1 ))
	# timed out
	[ ${iter} -gt ${_ttl} ] && notify && exit 1
done

# give time after the ping for sshd to start
sleep 3

notify
