# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

import yaml
from metux.util.log import info, warn
from metux.util.git import GitRepo
from metux.util.specobject import SpecObject

"""Package configuration"""
class PkgSpec(SpecObject):

    """split package identifier into name and (optional) version"""
    def _split_pkg_version(self, name):
        splitted = name.split('@',1)
        if (len(splitted) > 1):
            return (splitted[0], splitted[1])
        else:
            return (name, None)

    """[private]"""
    def _load_db(self, dbname):
        self._my_db[dbname] = self.conf.csdb.get_db(self.package_name, dbname)
        if self._my_db[dbname] is not None:
            self.default_addlist({
                dbname+'-url':    self._my_db[dbname].git_url,
                dbname+'-branch': self._my_db[dbname].git_branch,
            })

    """[private]"""
    def __init__(self, name, spec, conf):
        if spec is None:
            warn("pkg spec is None for package: "+name)
            spec = {}

        SpecObject.__init__(self, spec)

        self.conf = conf
        self.name = name
        self._my_db = {}

        ## split package name / version
        (self.package_name, self.package_version) = self._split_pkg_version(self.name)

        ## load repo configs from csdb
        for dbn in self.conf.csdb.get_dbnames():
            self._load_db(dbn)

        ## add variables for substitution
        self.default_addlist({
            'GLOBAL':          self.conf,
            'package.version': lambda: self.package_version,
            'package.name':    lambda: self.package_name,
            'package.fqname':  lambda: self.name,
            'package.src':     "${GLOBAL::pathes::pkg-prefix}${package.fqname}${GLOBAL::pathes::pkg-suffix}",
            'autobuild-local': 'autobuild',
        })

        # add global defaults
        self.default_addlist(self.conf['defaults','packages'])

    """get the global config"""
    def get_conf(self):
        return self.conf

    """get GitRepo instance"""
    def git_repo(self):
        return GitRepo(self['package.src'])

    """get url of remote repo <name>"""
    def git_remote_url(self, name):
        return self.get_cf(name+'-url')

    """get dependencies - package names)"""
    def get_depends_list(self):
        return self.get_cf_list('depends')

    """get dependencies - package objects"""
    def get_depends_packages(self):
        return self.conf.get_packages_by_names(self.get_depends_list())

    """get git repo config"""
    def get_repo_conf(self):
        remotes = {}
        for r in self.conf.get_remote_names():
            u = self.git_remote_url(r)
            if u is not None:
                remotes[r] = { 'url': u }
        return {
            'path':             self['package.src'],
            'remotes':          remotes,
            'init-branch':      self['autobuild-local'],
            'init-ref':         self['autobuild-ref'],
            'init-submodules':  self['init-submodules'],
            'init-force':       self['autobuild-force'],
        }

    """check whether package is skipped on given target"""
    def skipped_on_target(self, target):
        target_name = target['name']
        skiplist = self['skip-on-target']
        if skiplist is not None:
            for sk in skiplist:
                if sk == target_name:
                    return True

        return False
