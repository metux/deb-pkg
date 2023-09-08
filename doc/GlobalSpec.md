GlobalSpec (repository config)
==============================

The repository config (also called the global config) is the central starting point for all
operations. It basically declares what should be built into the final installable package
repository. Usually placed under `cf/repos/`.

### Root level keys:

key | description
---|---
targets  | Lists the target distros that will be built for
defaults | Global defaults for certain config items
packages | Lists the packages that can be built
pools    | The repo pools and their packages


Internally, this config is stored into the global scope. It's fields can be referenced from
other scopes via the `GLOBAL::` prefix.

Targets section
---------------

We can build installable repos for several distros in one pass. The `targets` list
*(list of strings)* defines which targets shall be used. Settings for individual targets defined
under `cf/targets`.

If predefined targets aren't sufficient, additional ones can be configured by adding appropriate
target config yaml files.

Note that different cpu architectures also imply different targets. In order to support classic
multiarch repos *(as most dpkg based distros do)*, the predefined targets are configured to place
their output into the same, per-distro, repository.

Example: the targets `devuan/daedalus/i386` and `devuan/deadalus/amd64` will both use target repo
name `devuan/daedalus`

Pools section
-------------

In order to support different building multiple repos with different package subsets, we can
configure separate pools. These are listed as subkeys under the `pools` root key. Each pool
defines a list of primary packages *(key "packages")* it should contain. If those also define
dependencies, these will be added automatically, thus being built and landing the repo.

Most cases *(for now)* should be sufficient w/ just one pool, named `default`.

The path of the finally installable repo will be a subdir, named by the pool, under the
per-target directory.

For future releases it is planned to support importing of pools into others: in this case, the
per-package build job will also add the imported pool's target repo *(so it's packages can be
directly used)* and skip building dependencies that are already supplied by the imported pools.
This allows better separation, eg. when some packages have some special build-only dependencies,
that shouldn't be shipped in the same target repo. *(classic case: golang packages often require
newer toolchain than shipped by the distro)*

Packages section:
-----------------

Under the `packages` section, all packages are defined - one subkey per package. The package key
may either be just the package name, or package name + `"@"` + version string. Inside the package
config, the fields `package.name` and `package.version` are automatically set.

The packages defined here are only built, when explicitly pulled in by a pool's package list or
as some other package's dependency.

See [PkgSpec](doc/PkgSpec.md)

Package config:
---------------

The package config defines everyhing needed for an individual package, which is loaded into a
separate object *(thus: separate variable namespace)*. When loaded from the global config, the
fields `package.fqname` *(the key)* `package.name` *(package name w/o version suffix)* and
`package.version` *(if version is present)* are automatically set from the package key.

Most of the common data, eg. source repo locations, is loaded from CSDB - looked up by the package
*name* *(w/o the version qualifier)*. See topic CSDB for details.

### Important fields:

variable | description
---|---
package.name    | *(intrinsic)* the name of the package, w/o version qualifier
package.version | *(intrinsic)* the version string *(if present)*
package.fqname  | *(intrinsic)* full package name, including version suffix
skip-on-targets | list of targets which skips the package
depends         | list of dependency packages
autobuild-ref   | git ref to check out by default
