alias portsql='sqlite3 /usr/local/share/sqlports'
alias portslol='make 2>&1 | /usr/ports/infrastructure/bin/portslogger .'
alias portspldc='make port-lib-depends-check'
alias portsldc='make lib-depends-check'
alias portsplif='diff -up pkg/PLIST.orig pkg/PLIST'
alias portstsilp='mv pkg/PLIST.orig pkg/PLIST'
alias portspy3plist='FLAVOR=python3 make REVISION=999 plist && sed -i /PYCACHE}.$/s,lib,\${MODPY_COMMENT}lib, pkg/PLIST'
alias portsrc='cd `make show=WRKSRC`'
alias portsfast='MAKE_JOBS=4 make'

portsdiff() { cvs diff > /usr/ports/mystuff/${PWD##*/}.diff  ; less /usr/ports/mystuff/${PWD##*/}.diff ;}
portslessdiff() { less /usr/ports/mystuff/${PWD##*/}.diff  ; }
portscp() { scp /usr/ports/mystuff/${PWD##*/}.diff virtie:/var/www/iota/ports/ && echo https://chown.me/iota/ports/${PWD##*/}.diff ;}
portspy3() { FLAVOR="python3" make "$@" ;}
portspy3and2() { make "$@" ; FLAVOR="python3" make "$@" ;}
portspygrep() { grep "$1" */py-*/Makefile ;}
portslib() { nm -g "$1" | cut -c10- | grep -e^T > /tmp/"$(pwd |xargs basename)" ;}
portsfind() { find /usr/ports -iname "${1}" -exec grep -iH ${2} {} \; ;}

