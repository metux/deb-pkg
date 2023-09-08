PkgSpec
=======

Package specs everyhing needed for an individual package. It's usually loaded from individual
entries of [GlobalSpec](doc/GlobalSpec.md)'s `packages` section - the key from there is stored
in the `package.fqname` intrinsic.

When loaded from the global config, the
fields `package.name` and `package.version` *(if version is present)* are automatically set from
the package key.

Most of the common data, eg. source repo locations, is loaded from CSDB - looked up by the package
*name* *(w/o the version qualifier)*. See topic CSDB for details.

Important fields:
---------------------

variable | description
---|---
package.name    | *(intrinsic)* the name of the package, w/o version qualifier
package.version | *(intrinsic)* the version string *(if present)*
package.fqname  | *(intrinsic)* full package name, including version suffix
skip-on-targets | list of targets which skips the package
depends         | list of dependency packages
autobuild-ref   | git ref to check out by default
