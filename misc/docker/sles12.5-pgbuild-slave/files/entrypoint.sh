#!/bin/bash

echo "entrypoint: $0 $1 $2 $3"

case "$1" in
    rebuild-src-rpm)
        shift
        if ! /rebuild-src-rpm "$@" ; then
            echo "==== $1 failed. keeping running for debug ===="
            cat
        fi
        exit $?
    ;;
    *)
        echo "unknown command: $1"
        exit 1
    ;;
esac

exit 2
