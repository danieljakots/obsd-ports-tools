#!/bin/sh

sqlite3 /usr/local/share/sqlports "SELECT FULLPKGPATH, BROKEN FROM Ports WHERE BROKEN is not NULL;"
