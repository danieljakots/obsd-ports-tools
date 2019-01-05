#!/bin/sh

sqlite3 /usr/local/share/sqlports "select FULLPKGPATH, VALUE from Broken WHERE ARCH = 'amd64';"
