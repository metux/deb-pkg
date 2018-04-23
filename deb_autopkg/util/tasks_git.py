from deb_autopkg.util.task import Task, TaskFail
from metux.git import GitRepo
from metux.log import warn, info
from metux.pypi import debian

"""Task: clone an git repo w/ initial checkout"""
class GitCloneTask(Task):

    def do_run(self):

        spec = self.param['spec']
        repo = GitRepo(spec['path'])
        repo.initialize()

        for remote in spec['remotes']:
            repo.set_remote(remote, spec['remotes'][remote]['url'])

        pypi = spec.get('pypi', None)
        if pypi is not None:
            ret = debian.create_package(pypi, repo)

        if not repo.is_checked_out():
            if (not 'init-ref' in spec) or (spec['init-ref'] is None):
                raise BaseException('cant checkout "'+spec['path']+'": autobuild-branch not defined')
            else:
                info("running initial checkout of "+spec['init-ref'])
                if not repo.checkout(spec['init-ref'], spec['init-branch']):
                    raise BaseException('cant checkout "'+spec['path']+'": git checkout failed')

        return True
