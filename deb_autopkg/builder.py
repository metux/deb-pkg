from util.task import TaskRunner
from tasks import pkg_build, pkg_clone, all_clone, pool_build, pool_upload, pool_deploy

class Builder:

    def __init__(self, conf, params = {}):
        self.conf = conf
        self.params = params

    def _run(self, task):
        return TaskRunner(task.name).runTask(task)

    def build_package(self, name, pool, params):
        if 'dontclone' in params:
            dontclone = params['dontclone']
        else:
            dontclone = False

        return self._run(pkg_build.alloc(self.conf, self.conf.get_package(name), pool, params))

    def clone_package(self, name):
        return self._run(pkg_clone.alloc(self.conf, self.conf.get_package(name)))

    def clone_all(self):
        return self._run(all_clone.alloc(self.conf))

    def build_pool(self, name):
        pool = self.conf.get_pool(name)
        if pool is None:
            raise Exception("undefined pool: "+name)
        return self._run(pool_build.alloc(self.conf, self.conf.get_pool(name)))

    def upload_pool(self, name):
        pool = self.conf.get_pool(name)
        if pool is None:
            raise Exception("undefined pool: "+name)
        return self._run(pool_upload.alloc(self.conf, self.conf.get_pool(name)))

    def deploy_pool(self, name):
        pool = self.conf.get_pool(name)
        if pool is None:
            raise Exception("undefined pool: "+name)
        return self._run(pool_deploy.alloc(self.conf, self.conf.get_pool(name)))

    def build_all(self):
        return self._run(build_all.alloc(self.conf))
