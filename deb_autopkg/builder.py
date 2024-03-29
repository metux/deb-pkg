# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from metux.util.task import TaskRunner
from .tasks import pkg_build, pkg_clone, all_clone, all_baseimage, pool_build, pool_upload, pool_deploy
from metux.util.specobject import SpecError

class Builder:

    def __init__(self, conf):
        self.conf = conf

    def _run(self, task):
        return TaskRunner(task.name).runTask(task)

    def build_package(self, name):
        return self._run(pkg_build.alloc(self.conf, self.conf.get_package(name)))

    def clone_package(self, name):
        return self._run(pkg_clone.alloc(self.conf, self.conf.get_package(name)))

    def clone_all(self):
        return self._run(all_clone.alloc(self.conf))

    def baseimage_all(self):
        return self._run(all_baseimage.alloc(self.conf))

    def build_pool(self, name):
        if name is None or name == '':
            name = self.conf['defaults::build-pool']

        if isinstance(name, list):
            r = True
            for n in name:
                if n is not None and n != '':
                    r = r and self.build_pool(n)
            return r

        pool = self.conf.get_pool(name)
        if pool is None:
            raise SpecError("undefined pool: "+name)
        return self._run(pool_build.alloc(self.conf, self.conf.get_pool(name)))

    def upload_pool(self, name):
        pool = self.conf.get_pool(name)
        if pool is None:
            raise SpecError("undefined pool: "+name)
        return self._run(pool_upload.alloc(self.conf, self.conf.get_pool(name)))

    def deploy_pool(self, name):
        pool = self.conf.get_pool(name)
        if pool is None:
            raise SpecError("undefined pool: "+name)
        return self._run(pool_deploy.alloc(self.conf, self.conf.get_pool(name)))
