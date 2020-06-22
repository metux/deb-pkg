import subprocess
from os.path import dirname

class RemoteNode:
    def __init__(self, hostname, user = 'root'):
        self.user     = user
        self.hostname = hostname
        self.login    = user+'@'+hostname
        self.ssh_cmd  = [ 'ssh', self.login, '--']

    def exec_simple(self, args):
        return subprocess.call(self.ssh_cmd+args)

    def exec_stdout(self, args):
        proc = subprocess.Popen(self.ssh_cmd+args, stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        return out.strip()

    def mkdir(self, pathname):
        self.exec_simple(['mkdir', '-p', pathname])

    def chown(self, owner, fn):
        if owner is not None:
            return self.exec_simple(['chown', '-R', owner, fn])
        return 0

    def upload_tree(self, source, dest):
        self.mkdir(dest)
        return subprocess.call(['scp', '-q', '-r', source, self.login+':'+dest])

    def file_put(self, src_file, target_file, owner = None):
        rc = subprocess.call(['scp', '-B', '-q', src_file, self.login+":/"+target_file])
        if (rc != 0):
            return rc
        return self.chown(owner, target_file)

    def file_read(self, fn):
        return self.exec_stdout(["cat", fn])

    def rmtree(self, fn):
        return self.exec_simple(["rm", "-Rf", fn])

    def exec_pipe(self, args):
        return subprocess.Popen(self.ssh_cmd+args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def exec_pipe_cb(self, args, cb):
        p = self.exec_pipe(args)

        for line in iter(p.stdout.readline, ""):
            cb(line.rstrip())

        return p.wait()
