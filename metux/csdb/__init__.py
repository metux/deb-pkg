
__all__ = [ "base", "generic" ]

import generic
from metux import log

class CSDB:
    def __init__(self, confpath):
        self.confpath = confpath
        self.db = {}
        if self.confpath is None:
            log.warn("No CSDB path specified. Cant load databases")
            return

        self.load_db('upstream')
        self.load_db('debian')
        self.load_db('oss-qm')
        self.load_db('oss-qm-pub')
        self.load_db('ci')

    """load generic database of given name"""
    def load_db(self, dbname):
        self.db[dbname] = generic.DB(self.confpath+"/"+dbname, dbname)

    """retrieve package from database of given name"""
    def get_db(self, pkg, dbname):
        return self.db[dbname].get(pkg)

    """retrieve list of names of all registered databases"""
    def get_dbnames(self):
        return list(self.db)
