# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from metux.util.task import Task
from .pkg_clone import alloc as pkg_clone_alloc
from .dckbp_clone import alloc as dckbp_clone_alloc
from .pkg_build_apt import alloc as pkg_build_apt_alloc
from .pkg_build_zypper import alloc as pkg_build_zypper_alloc

"""Task: build a package for a target"""
class PkgBuildTargetTask(Task):

    """[private]"""
    def __init__(self, param):
        Task.__init__(self, param)
        self.target   = param['target']
        self.conf     = param['conf']
        self.pkg      = param['pkg']

    """[override]"""
    def get_subtasks(self):
        if self.pkg.skipped_on_target(self.target):
            self.log_info("skipped on target %s" % self.target['name'])
            return []

        self.log_info("building on target %s" % self.target['name'])

        tasks = []

        tasks.append(pkg_clone_alloc(self.conf, self.pkg))

        for pkg in self.pkg.get_depends_packages():
            tasks.append(alloc(self.conf, pkg, self.target))

        packager = self.target.get_packager()
        if packager == 'apt':
            tasks.append(dckbp_clone_alloc(self.conf))
            tasks.append(pkg_build_apt_alloc(self.conf, self.pkg, self.target))
        elif packager == 'zypper':
            tasks.append(pkg_build_zypper_alloc(self.conf, self.pkg, self.target))
        else:
            self.fail('unknown packager "%s" for target %s' %
                        (packager, self.target['name']))

        return tasks

def alloc(conf, pkg, target):
    return conf.cached_task_alloc('build-pkg-target:'+target['name']+':'+pkg.name, PkgBuildTargetTask, { 'pkg': pkg, 'target': target })
