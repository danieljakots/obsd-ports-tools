#!/bin/sh

for _cat in /usr/ports/* ; do
	# not all files are a category directory
	if [[ ! -d "${_cat}" ]] ; then
		continue
	fi
	if [[ ! -f "${_cat}/Makefile" ]] ; then
		continue
	fi
	for _portpath in ${_cat}/* ; do
		if [[ ! -f "${_portpath}/Makefile" ]] ; then
			continue
		fi
		_port=$(basename "${_portpath}")
		_hook=$(grep -c "${_port}" ${_cat}/Makefile)
		if [[ "${_hook}" -lt 1 ]] ; then
			echo "${_portpath}"
			echo "${_hook}"
		fi
	done
done
