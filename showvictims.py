#!/usr/bin/env python3

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004

# Copyright (C) 2016 Daniel Jakots <vigdis@chown.me>

# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.

#           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

# 0. You just DO WHAT THE FUCK YOU WANT TO.

import sqlite3
import sys

def req(cur, victim, dep_type):
    rep = []
    for row in cur.execute("SELECT FULLPKGPATH FROM Ports WHERE " + dep_type + " LIKE ?", ('%'+victim+'%',)):
        rep.append("/usr/ports/" + row[0])

    return rep

def main():
    if len(sys.argv) == 1:
        print("usage: " + sys.argv[0] + " port [depends type (build, lib, run, test)]", file=sys.stderr)
        print("usage: " + sys.argv[0] + " py-babel", file=sys.stderr)
        sys.exit(1)

    port = str(sys.argv[1])

    try:
        conn = sqlite3.connect('/usr/local/share/sqlports')
    except sqlite3.OperationalError:
        print("install sqlports (doas pkg_add sqlports)", file=sys.stderr)
        sys.exit(1)

    cur = conn.cursor()
    if len(sys.argv) > 2:
        for dep_type in sys.argv[2:]:
            if dep_type == "run":
                dep_type = "RUN_DEPENDS"
            elif dep_type == "test":
                dep_type = "TEST_DEPENDS"
            elif dep_type == "lib":
                dep_type = "LIB_DEPENDS"
            elif dep_type == "build":
                dep_type = "BUILD_DEPENDS"
            for v in req(cur, port, dep_type):
                print(v)
    else:
        for dep_type in ["LIB_DEPENDS", "BUILD_DEPENDS", "RUN_DEPENDS", "TEST_DEPENDS"]:
            print("  " + dep_type)
            for v in req(cur, port, dep_type):
                print(v)

    conn.close()

if __name__ == '__main__':
    main()
