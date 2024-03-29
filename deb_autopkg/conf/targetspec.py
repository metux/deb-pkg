# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from .pkgspec import PkgSpec
from metux.util.log import warn
from metux.util.specobject import SpecObject, SpecError

"""Target configuration"""
class TargetSpec(SpecObject):

    """[private]"""
    def __init__(self, name, pool, conf, spec):
        SpecObject.__init__(self, spec)
        self.pool = pool
        self.conf = conf
        self.default_addlist({
            'GLOBAL':         conf,
            'POOL':           pool,
            'name':           name,
            'pool.name':      lambda: 'global' if self.pool is None else self.pool['pool.name'],
            'dck-buildpackage::target':   "${dck-buildpackage::target}",
            'apt-repo::ident':            "${name}",
            'apt-repo::path':             lambda: self.get_aptrepo_path(),
            'zyp-repo::ident':            "${name}",
            'zyp-repo::path':             lambda: self.get_zyprepo_path(),
        })

    def get_aptrepo_path(self):
        if self.pool is None:
            raise SpecError("no pool - dont have an aptrepo")
        else:
            return self.pool['pool.aptrepo']+'/'+self['apt-repo::ident']

    def get_zyprepo_path(self):
        if self.pool is None:
            raise SpecError("no pool - dont have an zyprepo")
        else:
            return self.pool['pool.zyprepo']

    """allocate a statfile object for the (per target) package build finish-marker"""
    def get_pkg_build_statfile(self, pkg):
        if isinstance(pkg,PkgSpec):
            pkgname = pkg.name
        else:
            pkgname = pkg

        return self.conf.get_statfile(
            "build."+self['pool.name']+"."+self['name']+"."+pkgname)

    def get_packager(self):
        p = self.get_cf('packager', None)
        if p is None:
            warn("Target %s has no packager specified. Defaulting to apt" % self['name'])
            return 'apt'
        return p
