#!/bin/ksh

set -eu

for _port in $(grep -E "^[0-9]" /usr/ports/infrastructure/db/user.list | awk '{print $4}')
do
	# remove subpackage stuff like databases/postgresql,-server
	_port=$(echo "${_port}" | awk -F ',' '{print $1}')
	[[ -s "${_port}" ]] && continue
	[[ -d "/usr/ports/${_port}" ]] || echo "${_port}"
done
