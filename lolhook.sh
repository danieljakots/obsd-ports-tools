#!/bin/sh

for _chat in /usr/ports/* ; do
	if [[ ! -d "${_chat}" ]] ; then
		continue
	fi
	if [[ ! -f "${_chat}/Makefile" ]] ; then
		continue
	fi
	#echo ${_chat}
	for _porcpath in ${_chat}/* ; do
		if [[ ! -f "${_porcpath}/Makefile" ]] ; then
			continue
		fi
		_porc=$(basename "${_porcpath}")
		#echo "${_porc}"
		hook=$(grep -c "${_porc}" ${_chat}/Makefile)
		if [[ $hook -lt 1 ]] ; then
			echo "${_porcpath}"
			echo $hook
		fi
	done
done
