#!/bin/sh

sqlite3 /usr/local/share/sqlports "select * from Broken WHERE ARCH = 'amd64';"
