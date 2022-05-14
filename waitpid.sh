#!/bin/sh

usage() {
	echo "usage: ${0##*/} PID" 1>&2
	exit 1
}

[ $# -eq 1 ] || usage

while kill -0 $1 2> /dev/null;
do
	sleep 0.1
done
