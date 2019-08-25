alias portsql='sqlite3 /usr/local/share/sqlports'
alias portslol='make 2>&1 | /usr/ports/infrastructure/bin/portslogger .'
alias portspldc='make port-lib-depends-check'
alias portsldc='make lib-depends-check'
alias portsplif='diff -up pkg/PLIST.orig pkg/PLIST'
alias portstsilp='mv pkg/PLIST.orig pkg/PLIST'
alias portspy3plist='FLAVOR=python3 make plist'
alias portsrc='cd `make show=WRKSRC`'
alias portsfast='MAKE_JOBS=4 make'

portsdiff() { cvs diff > /usr/ports/mystuff/${PWD##*/}.diff  ; less /usr/ports/mystuff/${PWD##*/}.diff ;}
portslessdiff() { less /usr/ports/mystuff/${PWD##*/}.diff  ; }
portscp() { scp /usr/ports/mystuff/${PWD##*/}.diff virtie:/var/www/iota/ports/ && echo https://chown.me/iota/ports/${PWD##*/}.diff ;}
portspy3() { FLAVOR="python3" make "$@" ;}
portspy3and2() { make "$@" ; FLAVOR="python3" make "$@" ;}
portspygrep() { (cd /usr/ports && grep "$1" */py-*/Makefile ) ;}
portslib() { nm -g "$1" | cut -c10- | grep -e^T > /tmp/"$(pwd |xargs basename)" ;}
portsfind() { find /usr/ports -iname "${1}" -exec grep -iH ${2} {} \; ;}
portsgrep() { ( cd /usr/ports && grep "$1" */*/Makefile */*/*/Makefile ) ;}



# This version for when not running PORTS_PRIVSEP=Yes
#vibak() { for i; do [ -f "$i.orig" ] || cp "$i" "$i.orig"; done; vi "$@" ; }

# For when running PORTS_PRIVSEP=Yes
function vibak { for i; do [ -f "$i.orig" ] || doas -u _pbuild cp "$i" "$i.orig"; done; doas -u _pbuild env HOME=/home/pbuild /usr/bin/vi "$@" ; }
