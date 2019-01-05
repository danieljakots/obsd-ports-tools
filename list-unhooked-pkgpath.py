#!/usr/bin/env python3

import os
import sqlite3
import sys

SQLPORTS = "/usr/local/share/sqlports"


def is_hooked(category, port):
    with open("/usr/ports/" + category + "/Makefile", "r") as f:
        return port in f.read()


if __name__ == '__main__':
    if os.path.isfile(SQLPORTS):
        conn = sqlite3.connect(SQLPORTS)
    else:
        print("install sqlports (doas pkg_add sqlports)", file=sys.stderr)
        sys.exit(1)

    cur = conn.cursor()
    for row in cur.execute("SELECT FULLPKGPATH FROM Ports;"):
        category, _, port = row[0].partition("/")
        # meh
        if "asterisk-sounds" in port or "kde4/l10n/" in port:
            continue
        # ignore subpackages, they're automatically built
        if ",-" in port:
            continue
        # remove trailing comas
        if port[-1:] == ",":
            port = port[:-1]
        if "/" in port:
            category = category + "/" + port.rpartition("/")[0]
            port = port.rpartition("/")[2]
        # ruby is weird
        if port[-7:] == ",ruby25" or port[-7:] == ",ruby24":
            port = port[:-7]
        if not is_hooked(category, port):
            print(f"{category}/{port}")
