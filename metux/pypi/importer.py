from metux import pypi, mkdir, extract_tar, rmtree
from metux.log import info
from os.path import abspath
from os import listdir
import registry

def branch_name(name, version):
    return 'pypi/upstream/'+version

# try to use version from spec
def git_import(name, gitrepo, version=None):
    pkg = registry.get_package(name)

    branch = branch_name(pkg.get_name(), pkg.get_version())
    if gitrepo.is_branch(branch):
        info("git importer: branch "+branch+" already exists. skipping")
        return {
            'gitrepo': gitrepo,
            'pkg':     pkg,
            'branch':  branch,
            'version': pkg.get_version(),
        }

    tmpdir = gitrepo.get_tmpdir()
    release = pkg.get_release(pkg.get_version())
    release.download(tmpdir)

    workdir = tmpdir+'/'+name+'/tree'

    extract_tar(
        tmpdir+'/'+release.get_filename(),
        workdir)

    gitrepo.import_initial_tree(
        workdir+'/'+listdir(workdir)[0],
        branch,
        'Tarball import from pypi: '+pkg.get_version())

    rmtree(tmpdir)

    return {
        'gitrepo': gitrepo,
        'pkg':     pkg,
        'branch':  branch,
        'version': pkg.get_version(),
    }
