#!/bin/sh -e

export PYTHONPATH=".:$PYTHONPATH"
export TERM="dumb"  # http://www.incenp.org/notes/2012/python-term-smm-fix.html

py_version=$(python -c 'import sys; print ".".join(map(str, sys.version_info[:2]))')
script_dir="build/scripts-$py_version"
version="$($script_dir/euca-version 2>&1 | sed -e 's/^euca2ools \([0-9]\.[0-9]\).*/\1/')"

mkdir -p man
for exe in $@; do
    echo $exe
    description="$($script_dir/$exe --help 2>&1 | python -c 'import sys; print sys.stdin.read().split("\n\n")[1]')"
    help2man -N --no-discard-stderr -S "euca2ools $version" -n "$description" --version-string "$version" -o man/$(basename $exe).1 $script_dir/$exe
    sed -i -e 's/^.SH DESCRIPTION/.SH SYNOPSIS/' \
           -e 's/usage: *//' \
           -e '/^\.IP/{/^\.IP/d}' \
           -e '/^\.PP/{s/^\.PP.*/.SH DESCRIPTION/}' \
           man/$(basename $exe).1
done
