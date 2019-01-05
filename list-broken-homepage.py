#!/usr/bin/env python3

import os
import sqlite3
import sys

import requests

SQLPORTS = "/usr/local/share/sqlports"
FAKE_U_A = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
)


if __name__ == "__main__":
    if os.path.isfile(SQLPORTS):
        conn = sqlite3.connect(SQLPORTS)
    else:
        print("install sqlports (doas pkg_add sqlports)", file=sys.stderr)
        sys.exit(1)

    cur = conn.cursor()
    for row in cur.execute(
        "SELECT HOMEPAGE, FULLPKGPATH, MAINTAINER FROM Ports WHERE HOMEPAGE NOT NULL;"
    ):
        homepage = row[0]
        fullpkgpath = row[1]
        # convert "blah <foo@example.com>" to "foo@"
        maintainer = "".join(row[2].rpartition("<")[2][:-1].rpartition("@")[0:2])
        if homepage[:4] != "http":
            continue
        osef = {"github", "kde", "cpan", "pypi.python.org"}
        ignore = 0
        for idgaf in osef:
            if idgaf in homepage:
                ignore = 1
        if ignore:
            continue
        headers = {"User-Agent": FAKE_U_A}
        try:
            g = requests.get(homepage, headers=headers)
        except requests.exceptions.SSLError:
            g.status_code = "SSL"
        except requests.exceptions.ConnectionError:
            g.status_code = "CON"
        if g.status_code != 200:
            print(
                "{:22}".format(fullpkgpath[:22]),
                "{:40}".format(homepage[:40]),
                "{:4}".format(g.status_code),
                maintainer,
            )
