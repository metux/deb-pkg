import requests
import json
from metux import mkdir
from urllib import urlretrieve

pypi_url = "https://pypi.org/pypi"

class Release:
    def __init__(self, pkg, data):
        self.pkg = pkg
        self.data = data

    def download(self, tmpdir):
        mkdir(tmpdir)
        return urlretrieve(self.data['url'], tmpdir+"/"+self.data['filename'])

    def get_filename(self):
        return self.data['filename']

    def get_version(self):
        return self.data['version']

class Package:
    def __init__(self, data):
        self.data = data

    def get_author(self):
        return self.data['info']['author']+" <"+self.data['info']['author_email']+">"

    def get_version(self):
        return self.data['info']['version']

    def get_name(self):
        return self.data['info']['name']

    def get_description(self):
        return self.data['info']['description']

    def get_release_data(self, release):
        if release not in self.data['releases']:
            return None

        for r in self.data['releases'][release]:
            if r['filename'].endswith(".whl"):
                pass
            else:
                return r

    def get_release(self, release):
        return Release(self, self.get_release_data(release))

def get_package(name):
    return Package(json.loads(requests.get(pypi_url+"/"+name+"/json").text))
