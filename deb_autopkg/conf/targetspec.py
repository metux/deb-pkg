from deb_autopkg.util.log import info

"""Target configuration"""
class TargetSpec(object):

    """[private]"""
    def __init__(self, cf, pool):
        if type(cf) == str:
            info("targetspec: conf is only name: "+cf)
            self.cf = { 'name': cf }
        else:
            info("targetspec: conf is object")
            self.cf = cf

        self.pool = pool

    def get_target_name(self):
        return self.cf['name']

    def get_arch_name(self):
        return self.cf['arch']

    def get_pool_name(self):
        if self.pool is None:
            return 'global'
        else:
            return self.pool.name

    def get_aptrepo_path(self):
        if self.pool is None:
            return None
        else:
            return self.pool.get_aptrepo_path()
