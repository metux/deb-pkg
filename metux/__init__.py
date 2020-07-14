from subprocess import call
from os.path import abspath
from os import chmod
import os
import stat

def mkdir(dirname):
    call(['mkdir', '-p', abspath(dirname)])

def rmtree(dirname):
    call(['rm', '-Rf', abspath(dirname)])

def setexec(fn):
    chmod(fn, os.stat(fn).st_mode | stat.S_IEXEC)
