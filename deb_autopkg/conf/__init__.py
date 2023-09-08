# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

__all__ = [ "targetspec", "poolspec", "pkgspec", "config" ]

from .targetspec import TargetSpec
from .poolspec import PoolSpec
from .pkgspec import PkgSpec
from .config import GlobalSpec

"""create new global config object and load config file"""
def load(fn):
    cf = GlobalSpec()
    cf.load(fn)
    return cf
