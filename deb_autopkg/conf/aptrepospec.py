from deb_autopkg.util.log import info

class AptRepoSpec:
    def __init__(self, cf):
        self._my_spec = cf
        info("loading repo config")
        info("pool:   %s" % self['pool'])
        info("target: %s" % self['target'])
        info("dist:   %s" % self['dist'])

    def __getitem__(self, key):
        if key in self._my_spec:
            return self._my_spec[key]
        return ''

    def get_name(self):
        return self['name']

    def get_target_name(self):
        return self['target']

    def get_pool_name(self):
        return self['pool']

    def get_dist_name(self):
        return self['dist']

    def get_comment(self):
        return self['comment']

def alloc_list(specs):
    ret = {}
    for key in specs:
        walk = specs[key]
        walk['name'] = key
        ret[key] = AptRepoSpec(walk)
    return ret
