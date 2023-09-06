CHANGES
=======

v0.2
----

* deb_autopkg: support default pool

  - when no pool is given to repo-build-pool, pick the default pool(s) to build from the config key "defaults::build-pool", which defaults to 'default'.

* cf: repos: devuan: config for container tools (master)

    - Add an example repo config building container tools for various Devuan releases (oss-qm master branches), including dependencies like newer golang toolchain.

* csdb: new packages

  - add nerdctl
  - debian: add golang-defaults
  - add containerd-cgroups
  - rename golang to golang-go

* cf: targets

  - add Devuan unstable (multiarch-repo)
  - add Devuan testing (multiarch-repo)
  - add Devuan beowulf (multiarch-repo)
  - add Devuan unstable chimaera (multiarch-repo)
  - add Devuan unstable daedalus (multiarch-repo)

* github CI workflow:

  - autobuild: drop runner.os and runner.arch from cache names
  - move builder setup steps to it's own composite action
  - cache rootfs tarballs

* tools: add simple pool builder tool

  - Simple command line util for building a pool from given config file.

* deb_autopkg:

   - allow packages to be skipped on specific targets
   - deb_autopkg: target and repo config via target/ configs
   - add support for default pool (when none given)
