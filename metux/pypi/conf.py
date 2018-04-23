import yaml
from metux.log import info

"""PyPi import configuration"""
class PyPiConf:
    def __init__(self, fn):
        self.spec = {}
        if fn is not None:
            with open(fn) as f:
                self.spec = yaml.safe_load(f)
                info("loaded pypi import config: "+fn)
        else:
            info("pypi import not configured")

    def get_package_names(self):
        if 'packages' not in self.spec:
            return []

        names = []
        for n in self.spec.get('packages', {}):
            names.append(n)
        return names

    def get_package(self, name, version = None):
        if version is None:
            info("PyPiConf: get package: name="+name+" no version")
        else:
            info("PyPiConf: get package: name="+name+" version="+version)

        if (self.spec is None) or ('packages' not in self.spec):
            info("PyPiConf: no packages defined")
            return

        if name in self.spec['packages']:
            info("PyPiConf: got package: "+name)
            p = self.spec['packages'][name]

            if not 'name' in p:
                p['name'] = name

            if not 'maintainer' in p:
                p['maintainer'] = self.spec['maintainer']

            if version is not None:
                p['version'] = version

            return p

        info("PyPiConf: package not defined: "+name)

    """return the global maintainer configuration"""
    def get_maintainer(self):
        return self.spec.get('maintainer', 'nobody <nobody@none.org>')

    """return list of all packages"""
    def get_all_packages(self):
        if 'packages' not in self.spec:
            return []

        pkglist = []
        for n in self.spec['packages']:
            pkglist.append(self.get_package(n))
        return pkglist
