from ..util.task import Task
from metux.git import GitRepo
from os import getuid, getgid
from os.path import abspath, basename
from subprocess import call, Popen, PIPE, check_output
from glob import glob
from metux import rmtree, mkdir, schroot
import shutil
import re

#
# Notes for schroot:
# * all directories must point within the calling user's home dir
#   (limitation of the schroot tool)
#
"""build for zypper (rpmbuild+friends)"""
class PkgBuildZypperTask(Task):

    """[private]"""
    def __init__(self, param):
        Task.__init__(self, param)
        self.target   = param['target']
        self.conf     = param['conf']
        self.pkg      = param['pkg']
        self.statfile = self.target.get_pkg_build_statfile(self.pkg)

        self.pkg.default_addlist({
            # defaults for user-configurable settings
            'rpm-name':                 '${package.name}',

            # internal settings
            'zypper.rpm.tmpdir':        '${user.home}/rpmbuild',
            'zypper.rpm.tmpdir.specs':  '${zypper.rpm.tmpdir}/SPECS',
            'zypper.rpm.tmpdir.srcs':   '${zypper.rpm.tmpdir}/SOURCES',
            'zypper.tarball.name':      lambda: self.get_tarball_name(),
            'zypper.tarball.pathname':  '${zypper.rpm.tmpdir}/SOURCES/${zypper.tarball.name}',
            'zypper.tarball.prefix':    lambda: self.get_tarball_prefix(),
            'zypper.specfile':          '${package.src}/${rpm-name}.spec',
        })

        self.containers = {
            'docker':  self.do_run_docker,
            'schroot': self.do_run_schroot,
        }

    def get_tarball_name(self):
        for l in check_output(["rpmspec", "-P", self.pkg['zypper.specfile']]).splitlines():
            m = re.search('^Source0:\s*(.*)$', l)
            if m is not None:
                return basename(m.group(1))
        return self.pkg['${package.name}-${package.version}.tar.gz']

    def get_tarball_prefix(self):
        for l in check_output(["rpmspec", "-P", self.pkg['zypper.specfile']]).splitlines():
            m = re.search('^%setup\s*(.*)$', l)
            if m is not None:
                args = m.group(1).split(' ')
                for idx, val in enumerate(args):
                    if val == '-n':
                        return args[idx+1]+"/"

        return '${package.name}-${package.version}/'

    def do_run(self):

        # clean the rpmbuild temp dir
        rmtree(self.pkg['zypper.rpm.tmpdir'])

        # clean recreate the srpm dir
        zyprepo_src = abspath(self.target['target.zyprepo']+'/srpm')
        rmtree(zyprepo_src)
        mkdir(zyprepo_src)

        # copy the spec file
        specdir = self.pkg['zypper.rpm.tmpdir.specs']
        mkdir(specdir)
        shutil.copy(self.pkg['zypper.specfile'], specdir);

        # create source tarball from git repo
        if (not self.pkg.git_repo().archive(
                output=abspath(self.pkg['zypper.tarball.pathname']),
                prefix=self.pkg['zypper.tarball.prefix'])):
            self.fail("zypper failed: git-archive call failed")

        # create source rpm
        if (call(["rpmbuild", "--target", self.target['arch'], "-bs", self.pkg['zypper.specfile']])):
            self.fail("zypper build failed: rpmbuild call failed")

        # copy the source rpm
        for s in glob(self.pkg['zypper.rpm.tmpdir']+'/SRPMS/*.src.rpm'):
            shutil.copy(s, zyprepo_src)

        # run the build in container
        container = self.target['container']
        if container not in self.containers:
            self.fail("unsupported container type: "+repr(container))

        ret = self.containers[container]()
        self.statfile.set(self.pkg.git_repo().get_head_commit())
        return ret

    def do_run_docker(self):
        container_name = "build-zypper-"+self.target['target.name']+"-"+self.pkg.package_name
        cache_volume   = "build-zypper-"+self.target['target.name']+"-zypcache"

        if (call(['docker',
                  'run',
                  '--rm',
                  '-e',
                  'UID='+str(getuid()),
                  '-v',
                  abspath(self.target['target.zyprepo'])+':/usr/src/packages/repo',
                  '--mount',
                  'source='+cache_volume+',target=/var/cache/zypp',
                  '-it',
                  self.target['zypper::docker::image'],
                  'rebuild-src-rpm',
                  self.pkg['rpm-name']])):
            self.fail("zypper build failed: rpmbuild call failed")

        return True

    def do_run_schroot(self):
        with schroot.create_session(self.target['zypper::schroot::image'], 'root') as session:
            if (session.call([self.target['zypper::schroot::script'],
                              self.pkg['rpm-name'],
                              self.target['target.zyprepo'],
                              ('%d:%d' % (getuid(), getgid())),
                              abspath(self.target['zypper::schroot::cache']),
                              self.target['arch'],
                             ])):
                self.fail("zypper build failed: rpmbuild call failed")

        return True

    """[override]"""
    def need_run(self):
        return not self.statfile.check(self.pkg.git_repo().get_head_commit())

def alloc(conf, pkg, target):
    return conf.cached_task_alloc('build-pkg-zypper:'+target['target.name']+':'+pkg.name, PkgBuildZypperTask, { 'pkg': pkg, 'target': target })
