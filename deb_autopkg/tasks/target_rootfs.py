# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from metux.util.task import Task
from os import environ
from copy import copy
from subprocess import call

"""build for apt (docker-buildpackage)"""
class TargetBaseimageTask(Task):

    """[private]"""
    def __init__(self, param):
        Task.__init__(self, param)
        self.target   = param['target']
        self.conf     = param['conf']

    def do_run(self):
        tgt       = self.target

        env = copy(environ)

        self.log_info('building rootfs for target "%s"' % tgt['name'])

        if (call([self.conf.get_dckbp_cmd(),
                  '--create-baseimage',
                  '--target',
                  self.target['dck-buildpackage::target']],
                 env=env) != 0):
            self.fail("rootfs build failed: "+tgt['name'])

        return True

def alloc(conf, target):
    return conf.cached_task_alloc('target-baseimage:'+target['name'], TargetBaseimageTask, { 'target': target })
