## General

### Q: How to start a build ?

Pick a config from `cf/repos/...` and call `repo-build-pool`:

    ./repo-build-pool cf/repos/devuan/sidplayfp.yml

This builds all pools listed under `defaults::build-pool`. To build a specific
pool:

    ./repo-build-pool cf/repos/devuan/sidplayfp.yml sidplayfp-release

### Q: What does 'pool' mean here ?

Pools organize sets of packages. Each pool gets its own apt repository under
`.aptrepo/<pool-name>/`. Pools can have different versions of the same
upstream package (e.g. stable release vs. master branch).

### Q: How to define which distros to build for ?

The `targets:` section in the config references target definitions under
`cf/targets/`. Each target specifies a dck-buildpackage container image.

### Q: How to handle inter-package dependencies ?

Add `depends:` to the package entry referencing another package by config name.
The builder resolves the dependency tree automatically and adds previously
built packages as apt sources during dependent builds.

### Q: How to force a rebuild ?

Remove the corresponding state file in `.stat/`. For example:

    rm .stat/build.default.devuan/excalibur/amd64.sidplayfp@3.0.2

## Configuration

### Q: What do the CSDB directories do ?

`cf/csdb/` holds git source configs in four layers:

- **upstream/** — original upstream repos
- **debian/** — debian packaging repos (if separate)
- **oss-qm/** — oss-qm forks with debianization branches
- **oss-qm-pub/** — public oss-qm repos

These populate `git.url` and `git.branch` for each package. Later layers
override earlier ones.

### Q: How does versioning work ?

Package names use `name@version` (e.g. `libresidfp@1.0.2`). The version part
is substituted into branch templates via `${package.version}`, so
`debian/maint-${package.version}` becomes `debian/maint-1.0.2`.

### Q: Can I have multiple pools with different versions ?

Yes. Define multiple pools in the config with different package versions.
Each pool has its own apt repository and build state.

### Q: How to build packages that aren't in the target distro yet ?

Add them as dependencies in the config. The builder will build them first and
add the pool's apt repo as an additional source for subsequent builds.

### Q: How to build for Devuan ? (debootstrap fails to find script)

Debian's debootstrap doesn't know Devuan release names. Symlink them:

    cd /usr/share/debootstrap/scripts
    sudo ln -s sid ascii
    sudo ln -s sid beowulf
    sudo ln -s sid chimaera
    sudo ln -s sid daedalus
    sudo ln -s sid excalibur

### Q: Where to get dck-buildpackage ?

    https://github.com/metux/docker-buildpackage

## Troubleshooting

### Q: Build fails with GPG signing errors ?

Ensure the signing key is set in the environment, or disable signing:

    export DCK_BUILDPACKAGE_SIGNKEY=none

### Q: Package build hangs ?

Check that Docker has enough resources (RAM, disk space). The base image
build can take a while on first run.
