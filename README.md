# deb-pkg — Debian packaging automation

Automates building Debian packages from debianized git repos, resolves
dependency trees, and publishes into apt repositories.

## Requirements

- [dck-buildpackage](https://github.com/metux/docker-buildpackage) — builds
  packages inside Docker containers for any target distribution
- Docker

## Quick start

```sh
# Build all packages in the default pool(s)
./repo-build-pool cf/repos/devuan/sidplayfp.yml

# Build a specific pool
./repo-build-pool cf/repos/devuan/sidplayfp.yml sidplayfp-release

# Build a single pool for another repo config
./repo-build-pool cf/repos/mixed/wine.yml
```

## Configuration

### Repo config (`cf/repos/<name>.yml`)

Defines targets, packages, and pools:

```yaml
targets:
    - devuan/excalibur/amd64
    - devuan/excalibur/i386

defaults:
    build-pool:
        - release
        - master
    packages:
        autobuild-ref:    oss-qm/debian/maint-${package.version}
        autobuild-local:  debian/maint-${package.version}

packages:
    foo@1.0:
    bar@master:
        depends:
            - foo@1.0

pools:
    release:
        packages:
            - foo@1.0
            - bar@master

    master:
        packages:
            - foo@master
            - bar@master
```

- **targets**: target distro/arch combinations (loaded from `cf/targets/`)
- **packages**: each entry is `name@version` — version is used in branch names
  via `${package.version}`. Dependencies reference other packages by their
  config name.
- **pools**: named sets of packages, each gets its own apt repo under
  `.aptrepo/<pool-name>/<ident>/`
- **build-pool**: default pool(s) built when none specified on CLI (can be a
  list); defaults to `'default'`

### CSDB (source database) — `cf/csdb/`

Four layers of git source configs, loaded in order (later overrides earlier):

| Directory | Purpose |
|-----------|---------|
| `upstream/` | Original upstream repo |
| `debian/` | Debian packaging repo |
| `oss-qm/` | oss-qm fork (usually debianized maintenance branch) |
| `oss-qm-pub/` | Public oss-qm repos |

Each CSDB entry is a YAML file (one per package) specifying `git.url` and
`git.branch`. The build system resolves `${package.version}` in branch names
(e.g. `debian/maint-${package.version}` → `debian/maint-1.0.2`).

### Target config (`cf/targets/<distro>/<release>/<arch>.yml`)

One YAML file per target, e.g. `devuan/excalibur/amd64.yml`:

```yaml
arch: amd64
packager: apt
dck-buildpackage:
    target: devuan-excalibur-amd64
apt-repo:
    suite: excalibur
    ident: devuan/excalibur
```

## Commands

### `repo-build-pool <config> [pool]`

Build all packages in a pool. If no pool given, builds all pools listed in
`defaults::build-pool`.

### `repo-build-baseimage <config>`

Build Docker base images (root filesystems) for all targets.

## Pool mechanism

- Each pool has its own apt repository at `.aptrepo/<pool-name>/<ident>/`
- Packages are built along the dependency tree defined in `depends:`
- Previously built packages are added as apt sources for subsequent builds
- Pool names should be prefixed for clarity (e.g. `sidplayfp-release`,
  `sidplayfp-master`) when multiple configs may coexist
- Build state is tracked in `.stat/` — delete state files to force rebuild

## Tools

### `dck-buildpackage`

The underlying build engine. Manages Docker containers matching the target
distro, runs `dpkg-buildpackage` inside, and handles cross-build deps.

Repo: https://github.com/metux/docker-buildpackage

## See also

- [FAQ](FAQ.md)
- [CHANGES](CHANGES.md)
- License: AGPL v3
- Contact: Enrico Weigelt, metux IT consult <info@metux.net>
