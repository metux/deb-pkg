#!/bin/bash

die() {
    echo "$*" >&2
    exit 1
}

[ -f .git/config ] || die "need to be called from pkg git repo"

TMPNAME=`mktemp --dry-run tmp-import-XXXXXX`

log_info() {
    echo "[INFO] $*"
}

git_check_branch() {
    if git rev-parse --quiet --verify "$1" >/dev/null 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

debimport_dfsg_on_upstream() {
    [ "$UPSTREAM_REF"       ] || die "missing \$UPSTREAM_REF"
    [ "$DFSG_REF"           ] || die "missing \$DFSG_REF"
    [ "$IMPORT_DFSG_BRANCH" ] || die "missing \$IMPORT_DFSG_BRANCH"

    if git_check_branch "$IMPORT_DFSG_BRANCH" ; then
        log_info "dfsg import branch $IMPORT_DFSG_BRANCH already exists"
        return 0
    fi

    ## fork from upstream release tag into our dfsg-import branch
    git checkout -f "$UPSTREAM_REF" -b "$IMPORT_DFSG_BRANCH" || die "failed to fork dfsg import branch"

    ## copy over debian's dfsg tree
    git read-tree "$DFSG_REF" || die "failed to import dfsg tree"

    ## commit the changes
    git commit -m "dfgs-import from $DFSG_REF" || die "failed to commit dfsg tree"

    ## cleanup
    git clean -f -d || die "failed to cleanup"
}

import_from_debian() {
    IMPORT_DFSG_BRANCH="debian/dfsg-$UPSTREAM_VERSION"
    debimport_dfsg_on_upstream
}

import_v17_1() {
    UPSTREAM_VERSION="17.1"
    UPSTREAM_REF="$UPSTREAM_VERSION-Krypton"
    DFSG_REF="upstream/$UPSTREAM_VERSION+dfsg1"
    import_from_debian
}

import_v17_3() {
    UPSTREAM_VERSION="17.3"
    UPSTREAM_REF="$UPSTREAM_VERSION-Krypton"
    DFSG_REF="upstream/17.3+dfsg1"
    import_from_debian
}

import_v17_6() {
    UPSTREAM_VERSION="17.6"
    UPSTREAM_REF="$UPSTREAM_VERSION-Krypton"
    DFSG_REF="upstream/17.6+dfsg1"
    import_from_debian
}

## version 17.1
#UPSTREAM_VERSION="17.1" \
#    UPSTREAM_REF="$UPSTREAM_VERSION-Krypton" \
#    DFSG_REF="upstream/$UPSTREAM_VERSION+dfsg1" \
#    import_from_debian

#    IMPORT_DFSG_BRANCH="debian/dfsg-$UPSTREAM_VERSION" \
#    DEBIAN_REF="debian/2%17.1+dfsg1-3" \

import_v17_1
import_v17_3
import_v17_6
