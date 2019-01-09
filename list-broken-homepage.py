#!/usr/bin/env python3

import os
import sqlite3
import sys

import requests

SQLPORTS = "/usr/local/share/sqlports"
FAKE_U_A = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
)


def get_all_homepages():
    """Get all distinct homepages used in ports."""
    conn = sqlite3.connect(SQLPORTS)
    cur = conn.cursor()
    for row in cur.execute(
        "SELECT DISTINCT HOMEPAGE FROM _Ports WHERE HOMEPAGE IS NOT NULL;"
    ):
        yield row[0]


def check_homepage(homepage):
    """Try to connect to the homepage."""
    # work around HOMEPAGE ?= http;//drupal.org/project/${MODDRUPAL_PROJECT}/
    if homepage[:5] == "http;":
        return homepage, 200
    print(homepage, file=sys.stderr)
    headers = {"User-Agent": FAKE_U_A}
    try:
        g = requests.get(homepage, headers=headers, timeout=15)
        status_code = g.status_code
    except requests.exceptions.SSLError:
        status_code = "SSL"
    except requests.exceptions.ConnectionError:
        status_code = "CON"
    except requests.exceptions.ReadTimeout:
        status_code = "TMO"
    return homepage, status_code


def get_all_ports(homepage):
    """Get all the ports using a given homepage."""
    conn = sqlite3.connect(SQLPORTS)
    cur = conn.cursor()
    for row in cur.execute(
        """SELECT DISTINCT _Paths.FULLPKGPATH, _Email.VALUE
            FROM _Ports, _Email, _Paths
            WHERE _Ports.MAINTAINER = _Email.KEYREF
              AND _Ports.FULLPKGPATH = _Paths.ID
              AND _Paths.PKGPATH = _Paths.ID
              AND _Ports.HOMEPAGE = ?;""",
        (homepage,),
    ):
        fullpkgpath = row[0]
        maintainer = row[1]
        yield (fullpkgpath, maintainer)


def main():
    """Where everything happens. (TM)"""
    for homepage in get_all_homepages():
        # ignore non web stuff (ftp, gopher)
        if homepage[:4] != "http":
            continue
        homepage, status_code = check_homepage(homepage)
        if status_code == 200:
            continue
        for port in get_all_ports(homepage):
            fullpkgpath = port[0]
            # convert "blah <foo@example.com>" to "foo@"
            maintainer = "".join(port[1].rpartition("<")[2][:-1].rpartition("@")[0:2])
            print(
                "{:21}".format("|" + fullpkgpath[:20]),
                "{:33}".format(homepage[:33]),
                "{:3}".format(status_code),
                "{:7}".format(maintainer[:7]),
                sep="|",
                end="",
            )
            print("|")


if __name__ == "__main__":
    if not os.path.isfile(SQLPORTS):
        print("install sqlports (doas pkg_add sqlports)", file=sys.stderr)
        sys.exit(1)

    print("CON = couldn't connect (might be DNS), TMO = Timeout, SSL = SSL")
    # print a nice table
    print("+" + 20 * "-" + "+" + 33 * "-" + "+" + 3 * "-" + "+" + 7 * "-" + "+")
    main()
    print("+" + 20 * "-" + "+" + 33 * "-" + "+" + 3 * "-" + "+" + 7 * "-" + "+")
    print("CON = couldn't connect (might be DNS), TMO = Timeout, SSL = SSL")
