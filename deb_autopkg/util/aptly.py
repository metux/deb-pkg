from log import info, warn
import subprocess

class Aptly:
    def __init__(self, aptrepo):
        self.repo = aptrepo
        self.name = aptrepo.get_name()
        self.init()

    def init(self):
        return subprocess.call([
            'aptly',
            'repo',
            'create',
            '-comment',
            self.repo['comment'],
            self.repo['name']
        ])

    def add_pkg(self, debfile):
        info("Adding to repo "+self.name+": " +debfile)
        return subprocess.call([
            'aptly',
            'repo',
            'add',
            self.repo['name'],
            debfile
        ])

    def update(self):
        info("Updating / republishing repo "+self.name)
        return subprocess.call([
            'aptly',
            'publish',
            'update',
            self.repo['name']
        ])
