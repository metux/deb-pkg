import yaml
from metux.log import info

def _fixup_name(name):
    if name.startswith('python-'):
        return name[7:]
    elif name.startswith('python3-'):
        return name[8:]
    elif name.startswith('python2-'):
        return name[8:]

"""PyPi import configuration"""
class PyPiConf(object):
    def __init__(self, fn):
        self.spec = {}
        if fn is not None:
            with open(fn) as f:
                self.spec = yaml.safe_load(f)
                info("loaded pypi import config: "+fn)
        else:
            info("pypi import not configured")

    def get_package(self, name, version = None):
        name = _fixup_name(name)

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
