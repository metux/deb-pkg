# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from .builder import Builder
from .conf import load
from metux.util.specobject import SpecError
from metux.util.task import TaskFail
from metux.util.log import err
import functools

def cmdfunc(func):
    @functools.wraps(func)
    def wrapper_cmdfunc(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return 0
        except TaskFail as ex:
            err("[%s] %s" % (ex.get_task_name(), ex.get_message()))
            return 127
        except SpecError as ex:
            err("[config error] %s" % ex.get_message())
            return 126
    return wrapper_cmdfunc

@cmdfunc
def build_pool(conffile, pool):
    return Builder(load(conffile)).build_pool(pool)

@cmdfunc
def upload_pool(conffile, pool):
    return Builder(load(conffile)).upload_pool(pool)

@cmdfunc
def deploy_pool(conffile, pool):
    return Builder(load(conffile)).deploy_pool(pool)

@cmdfunc
def build_all(conffile):
    return Builder(load(conffile)).build_all()

@cmdfunc
def build_package(conffile, pkg):
    return Builder(load(conffile)).build_package(pkg)

@cmdfunc
def clone_all(conffile):
    return Builder(load(conffile)).clone_all()

@cmdfunc
def baseimage_all(conffile):
    return Builder(load(conffile)).baseimage_all()

@cmdfunc
def get_builder(conffile):
    return Builder(load(conffile))

@cmdfunc
def get_dut(conffile, name):
    return load(conffile).get_dut(name)

@cmdfunc
def dut_exec(conffile, dutname, cmd = []):
    return get_dut(conffile, dutname).dut_exec(cmd)

@cmdfunc
def pool_invalidate_target_package(conffile, poolname, pkgname, targetname):
    get_builder(conffile).conf.get_pool(poolname).invalidate_target_package(pkgname, targetname)
    return True

@cmdfunc
def tool_repo_build_pool(argv):
    if len(argv) < 2:
        print("%s <config-file> [pool]" % argv[0])
        print("")
        print("Build a package repo pool from given config file")
        print("If no pool given, the setting defaults::build-pool is used (defaults to 'default')")
        return 1

    if len(argv) < 3:
        return build_pool(argv[1], None)

    return build_pool(argv[1], argv[2])

@cmdfunc
def tool_repo_build_rootfs(argv):
    if len(argv) < 2:
        print("%s <config-file>" % argv[0])
        print("")
        print("Build root filesystems for targets in given config file")
        return 1

    return baseimage_all(argv[1])
