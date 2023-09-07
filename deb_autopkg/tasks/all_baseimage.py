# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from metux.util.task import Task
from .target_rootfs import alloc as target_rootfs_alloc
from .dckbp_clone import alloc as dckbp_clone_alloc

""" Task: clone all package git repos"""
class BaseimageAllTask(Task):

    def get_subtasks(self):
        conf = self.param['conf']
        tasks = [ dckbp_clone_alloc(conf) ]

        for t in conf.get_targets():
            tasks.append(target_rootfs_alloc(conf, t))

        return tasks

def alloc(conf):
    return conf.cached_task_alloc('baseimage-all', BaseimageAllTask, { 'conf': conf })
