from metux import write_file, setexec, rmtree
from metux.log import info, warn, err
from shutil import copyfile
from string import Template
from os import path
from importer import git_import
from pkginfo import Develop
from os.path import isfile, abspath, dirname
from metux.git import GitRepo
import yaml
from conf import PyPiConf

"""
fixup package name:
underscores are not allowed, so replace by dash
"""
def fixname(name):
    return name.replace('_','-')

def branch_name(name, version):
    return "pypi/debian/"+version

"""Generate debian packaging control files"""
class ControlGen:

    # FIXME: try to use version from spec
    def __init__(self, spec, pkg, worktree):
        self.spec       = spec
        self.pkg        = pkg
        self.name       = fixname(pkg.get_name())
        self.version    = pkg.get_version()
        self.worktree   = worktree
        self.var        = {
            'maintainer': spec['maintainer'],
            'version':    pkg.get_version(),
            'package':    self.name,
            'src_pkg':    'python-'+self.name,
            'py2_pkg':    'python-'+self.name,
            'py3_pkg':    'python3-'+self.name,
        }
        self.load_pkginfo()
        self.load_depends()

    def load_template(self, name):
        path = dirname(abspath(__file__))+'/dpkg-templates/'+name+'.in'
        with open(path, 'r') as content_file:
            return Template(content_file.read())

    def do_template(self, name):
        write_file(self.wd_fn(name), self.load_template(name).substitute(self.var))

    def _wr_ctl(self, fn, content):
        write_file(self.wd_fn('debian/'+fn), content)

    def setvar(self, name, val, dfl = ''):
        if val is None:
            self.var[name] = dfl
        else:
            self.var[name] = val

    """load package metadata from PKG-INFO file"""
    def load_pkginfo(self):
        try:
            p = Develop(self.worktree)
            self.setvar('description', p.description, '(no description)')
            self.setvar('summary',     p.summary, 'Python package: '+self.name)
            self.setvar('homepage',    p.home_page, "http://pypi.python.org/pypi/"+self.name)
            self.setvar('license',     p.license)
        except:
            warn("Cant load PKG-INFO metadata ... skipping")

    def getlist(self, n):
        if n in self.spec:
            return self.spec[n]
        else:
            return []

    def setdeps(self, name, deps):
        if len(deps) > 0:
            self.setvar(name, ", "+", ".join(deps))
        else:
            self.setvar(name, '')

    """
    translate pypi package names to debian source

    pypi-py2-depends => python-*
    pypi-py3-depends => python3-*
    pypi-all-depends => python-* python3-*
    """
    def load_depends(self):
        alldeps = self.getlist('pypi-all-depends')

        trans_py2  = ['python-'+s  for s in self.getlist('pypi-py2-depends')]
        trans_py3  = ['python3-'+s for s in self.getlist('pypi-py3-depends')]
        trans_all2 = ['python-'+s  for s in alldeps]
        trans_all3 = ['python3-'+s for s in alldeps]

        self.setdeps('src_depends', trans_py2 + trans_py3 + trans_all2 + trans_all3)
        self.setdeps('py2_depends', trans_py2 + trans_all2)
        self.setdeps('py3_depends', trans_py3 + trans_all3)

    """generate filename relative to current worktree directory"""
    def wd_fn(self, fn):
        return self.worktree+'/'+fn

    """create a .gitignore file is not existing yet"""
    def write_gitignore(self):
        if not isfile(self.wd_fn('.gitignore')):
            self.info("creating .gitignore file")
            self.do_template('.gitignore')

    """copy well-known copyright files"""
    def write_copyright(self):
        if isfile(self.wd_fn('LICENSE')):
            self.info("copy LICENSE to debian/copyright")
            copyfile(self.wd_fn('LICENSE'), self.wd_fn('debian/copyright'))

    """write out files from templates"""
    def write_templates(self):
        tmpl = [
            'debian/changelog',
            'debian/rules',
            'debian/copyright',
            'debian/compat',
            'debian/control',
            'debian/source/format',
            'debian/source/options',
            'debian/patches/series',
            'debian/.gitignore',
        ]
        for name in tmpl:
            self.info("creating "+name)
            self.do_template(name)

        setexec(self.wd_fn('debian/rules'))

    """write the *.install files"""
    def write_install(self):
        self._wr_ctl(self.var['py2_pkg']+'.install', "/usr/lib/python2.*\n")
        self._wr_ctl(self.var['py3_pkg']+'.install', "/usr/lib/python3.*\n")

    """write the debian packaging files"""
    def write(self):
        self.write_templates()
        self.write_install()
        self.write_copyright()
        self.write_gitignore()

    def info(self, text):
        info("["+self.name+"] "+text)

def create_package(spec, gitrepo):
    res = git_import(spec['name'], gitrepo=gitrepo, version=spec.get('version', None))
    pkg = res['pkg']
    branch = branch_name(pkg.get_name(), pkg.get_version())

    if gitrepo.is_branch(branch):
        info("branch "+branch+" already exists. skipping")
        return

    workdir = gitrepo.get_tmpdir()

    gitrepo.extract_tree(workdir, res['branch'])

    ControlGen(spec, pkg, workdir).write()

    gitrepo.remove_branch(branch)
    gitrepo.import_initial_tree(
        workdir,
        branch,
        'Auto debianization: '+pkg.get_version(),
        parent = res['branch'])

    rmtree(workdir)

    return {
        'package':         pkg.get_name(),
        'version':         pkg.get_version(),
        'upstream-branch': res['branch'],
        'debian-branch':   branch,
    }

def __create_gitrepo(spec):
    if 'version' in spec:
        suffix = '@'+spec['version']
    else:
        suffix = ''

    r = GitRepo('pkg/python-'+spec['name']+suffix+'.git')
    r.initialize()
    return r

def run_auto_import(fn):
    conf = PyPiConf(fn)

    for pkg in conf.get_all_packages():
        create_package(pkg, __create_gitrepo(pkg))
