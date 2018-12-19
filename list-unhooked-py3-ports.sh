#!/bin/sh

for _pkgpath in $(sqlite3 /usr/local/share/sqlports "select FULLPKGPATH from Ports where FULLPKGPATH like '%,python3';") ; do
	_cat=$(echo "${_pkgpath}" | awk -F '/' '{print $1}')
	_port=$(echo "${_pkgpath}" | awk -F '/' '{print $2}')
	_hook=$(grep -c "${_port}" "/usr/ports/${_cat}/Makefile")
	if [[ "${_hook}" -lt 1 ]] ; then
		echo "${_cat}/${_port}"
	fi
done
