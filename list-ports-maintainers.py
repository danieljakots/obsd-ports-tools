import sqlite3

SQLPORTS = "/usr/local/share/sqlports"

maintainers = [
    "foo",
    "bar",
]

conn = sqlite3.connect(SQLPORTS)
cur = conn.cursor()
for maintainer in maintainers:
    cur.execute(
        "SELECT DISTINCT _Paths.FULLPKGPATH FROM _Ports, _Email, _Paths WHERE _Ports.FULLPKGPATH = _Paths.ID AND _Paths.PKGPATH = _Paths.ID AND _Ports.MAINTAINER = _Email.KeyRef AND _Email.Value like ?",
        (f"%{maintainer}%",),
    )
    print(' '.join(''.join(e) for e in cur.fetchall()), end=' ')
