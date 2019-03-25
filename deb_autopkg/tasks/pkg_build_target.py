from deb_autopkg.util.task import Task
from metux.log import info
from os import environ
from copy import copy
from subprocess import call

import pkg_clone
import dckbp_clone

"""Task: build a package for a target"""
class PkgBuildTargetTask(Task):

    """[private]"""
    def __init__(self, param):
        Task.__init__(self, param)
        self.target   = param['target']
        self.conf     = param['conf']
        self.pkg      = param['pkg']
        self.statfile = self.conf.get_statfile(
            "build."+self.target.get_pool_name()+"."+self.target.get_target_name()+"."+self.pkg.name)
        self.dontclone = self.get_param_bool('dontclone', False)

    """[override]"""
    def get_subtasks(self):
        tasks = []
        tasks.append(dckbp_clone.alloc(self.conf))
        if self.dontclone:
            info("PkgBuildTargetTask: not cloning")
        else:
            tasks.append(pkg_clone.alloc(self.conf, self.pkg))

        for pkg in self.pkg.get_depends_packages():
            tasks.append(alloc(self.conf, pkg, self.target, self.dontclone))

        return tasks

    """[override]"""
    def need_run(self):
        return not self.statfile.check()

    """[override]"""
    def do_run(self):
        pkg_name    = self.pkg.name
        target_name = self.target.get_target_name()
        pool_name   = self.target.get_pool_name()
        dckbp_cmd   = self.conf.get_dckbp_cmd()

        env = copy(environ)
        env['DCK_BUILDPACKAGE_TARGET_REPO'] = self.target.get_aptrepo_path()
        env['DCK_BUILDPACKAGE_SOURCE'] = pkg_name

        info('building "'+pkg_name+'" from '+pool_name+' for '+target_name)
        if (call([dckbp_cmd, '--target', target_name],
                 cwd=self.pkg.git_repo_dir(),
                 env=env) != 0):
            self.fail("build failed: "+pkg_name)

        self.statfile.set()
        return True

def alloc(conf, pkg, target, dontclone = False):
    return conf.cached_task_alloc('build-pkg-target:'+target.get_target_name()+':'+pkg.name,
                                  PkgBuildTargetTask,
                                  { 'pkg': pkg, 'target': target, 'dontclone': dontclone })
