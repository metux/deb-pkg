#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>
#
# Emit the GitHub Actions build matrix as JSON.
#
# Each matrix entry is one (config-file x pool) combination. A pool is built
# across all targets (distro/arch) listed in its config, which keeps any
# intra-pool "depends:" ordering intact (the matrix never splits a dependency
# chain across jobs). Targets and pools are read straight from cf/repos/*.yml,
# so the matrix stays data-driven.
#
# Output (one line, for $GITHUB_OUTPUT):
#   matrix={"include":[{"config":..,"pool":..,"name":..,"artifact":..}, ...]}

import glob
import json
import os
import re
import sys

import yaml


def slugify(text):
    return re.sub(r'[^A-Za-z0-9._-]+', '-', text).strip('-')


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else 'cf/repos'
    include = []

    for conf in sorted(glob.glob(os.path.join(root, '**', '*.yml'), recursive=True)):
        with open(conf) as f:
            data = yaml.safe_load(f) or {}
        pools = (data.get('pools') or {})
        # config path relative to repo root, e.g. cf/repos/devuan/go-x11.yml
        repo_id = os.path.splitext(os.path.relpath(conf))[0]
        for pool in pools.keys():
            name = '%s / %s' % (repo_id.replace('cf/repos/', ''), pool)
            artifact = 'aptrepo-' + slugify(repo_id + '-' + pool)
            include.append({
                'config': conf,
                'pool': pool,
                'name': name,
                'artifact': artifact,
            })

    matrix = {'include': include}
    out = 'matrix=' + json.dumps(matrix, separators=(',', ':'))

    gh_out = os.environ.get('GITHUB_OUTPUT')
    if gh_out:
        with open(gh_out, 'a') as f:
            f.write(out + '\n')
    print(out)


if __name__ == '__main__':
    main()
