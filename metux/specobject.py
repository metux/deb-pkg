import yaml
from os import getuid, getcwd, getgid
from os.path import expanduser
from metux.log import info
from metux.lambdadict import LambdaDict
from string import Template
import re

class SubstTemplate(Template):
    idpattern = r"[\@_a-zA-Z][_a-zA-Z0-9/\.\-\:]*"

class SpecObject(object):

    """[private]"""
    def __init__(self, spec):
        self.set_spec(spec)

    """retrieve a config element by path"""
    def get_cf_raw(self, p, dflt = None):
        res = self._my_spec[p]
        if res is None:
            return dflt
        else:
            return res

    """retrieve a config element as list"""
    def get_cf_list(self, p, dflt = []):
        return self.get_cf(p, dflt)

    """retrieve a config element by path and substitute variables"""
    def get_cf(self, p, dflt = None):
        return self.cf_substvar(self.get_cf_raw(p, dflt))

    """retrieve the first in a list of keys which returs non-None"""
    def get_cf_either(self, plist, dflt=None):
        for p in plist:
            r = self.get_cf(p)
            if r is not None:
                return r
        return dflt

    """retrieve a config element as dict"""
    def get_cf_dict(self, p):
        r = self.get_cf(p)
        if p is None:
            return LambdaDict({})
        return r

    """retrieve a config element as bool"""
    def get_cf_bool(self, p, dflt = False):
        r = self.get_cf(p, dflt)
        if r is None:
            return dflt
        if r:
            return True
        return False

    """container get method"""
    def __getitem__(self, p):
        return self.get_cf(p)

    """set spec object"""
    def set_spec(self, s):
        self._my_spec = LambdaDict(s)
        self.default_addlist({
            'user.uid':       lambda: str(getuid()),
            'user.gid':       lambda: str(getgid()),
            'user.home':      lambda: expanduser('~'),
            'user.cwd':       lambda: getcwd(),
            '@STRLINES':      XfrmStrLines(self),
            '@STRLIST':       XfrmStrList(self),
            '@YESNO':         XfrmYesNo(self),
            '@PROPS':         XfrmProps(self),
        })

    """get spec object"""
    def get_spec(self, s):
        return self._my_spec

    """def load spec from yaml"""
    def load_spec(self, fn):
        with open(fn) as f:
            # use safe_load instead load
            self.set_spec(yaml.safe_load(f))
            info("loaded config: "+fn)

    """add a default value, which will be used if key is not present"""
    def default_set(self, key, val):
        self._my_spec.default_set(key, val)

    """add a list of default values"""
    def default_addlist(self, attrs):
        self._my_spec.default_addlist(attrs)

    """[private] variable substitution"""
    def cf_substvar(self, var):

        if var is None:
            return None

        if (var is None) or (isinstance(var,bool)) or (isinstance(var, (long, int))):
            return var

        if isinstance(var, basestring) or (isinstance(var, str)):
#            if var.lower() in ['true', 't', 'y', 'yes']:
#                return True
#
#            if var.lower() in ['false', 'f', 'n', 'no']:
#                return False

            m = re.match(r"^\$\{([_a-zA-Z][_a-zA-Z0-9/\.\-\:]*)}$", var, re.M|re.I)
            if m:
                return self[m.group(1)]

            new = SubstTemplate(var).substitute(self._my_spec)
            if new == var:
                return var

            return self.cf_substvar(new)

        return var

class PrefixSpecObject(SpecObject):

    def __init__(self, parent, prefix):
        self.parent = parent
        self.prefix = prefix

    """retrieve a config element by path and substitute variables"""
    def get_cf(self, key, dflt = None):
        if type(key)==tuple:
            return self.parent.get_cf((self.prefix,)+key, dflt)
        if type(key)==list:
            return self.parent.get_cf([self.prefix]+key, dflt)
        return self.parent.get_cf(self.prefix+'::'+key, dflt)

    def default_set(self, key, val):
        raise Exception("default_set() not supported")

    """add a list of default values"""
    def default_addlist(self, attrs):
        raise Exception("default_addlist() not supported")

class XfrmBase(SpecObject):

    def __init__(self, parent):
        self.parent = parent

class XfrmStrLines(XfrmBase):

    def get_cf(self, key, dflt = ""):
        var = self.parent.get_cf(key, dflt)
        s= "" if var is None else "\n".join(var)
        return s

class XfrmYesNo(XfrmBase):

    def get_cf(self, key, dflt = False):
        x = self.parent.get_cf_bool(key, dflt)
        return "yes" if x else "no"

class XfrmProps(XfrmBase):

    def get_cf(self, key, dflt = ""):
        var = self.parent.get_cf(key, dflt)
        if var is None:
            return dflt
        return "\n".join([name+" "+url for name, url in var.iteritems()])

class XfrmStrList(XfrmBase):

    def get_cf(self, key, dflt = ""):
        var = self.parent.get_cf(key, dflt)
        if var is None:
            return dflt
        return " ".join(var)
