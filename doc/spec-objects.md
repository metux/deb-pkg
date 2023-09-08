Specification objects
=====================

The configuration of the build process is comprised of several specification objects - these
have tree-structured attributes, loaded from YAML files. Some attributes have intrinsic defaults,
resolved at runtime *(when the value is retrieved)*.

Spec objects also may have references to other ones *(via intrinsics)*, all have a reference to
the GlobalSpec *(as `GLOBAL::`).

Variable substitution
---------------------

Scalar **values** *(single items, list entries, but not struct keys)* support variable substitution:

    foo: x-${bar}

    list:
      - ${foo}
      - y-${bar}

Nested variables may be addressed by a path:

    one:
      two:
        three: ABC

    foo: ${one::two::three}

Path addressing also works through intrinsic object references:

    ${GLOBAL::config.basedir}/cf
    ${GLOBAL::pathes::github::current}oss-qm/

Defaults and intrinsics
-----------------------

Spec objects may have defaults set by other places. Intrinsics are defaults defined by the objects
themselves, usually functions or references to other SpecObject's.


Object types
------------

* [GlobalSpec](GlobalSpec.md)
  * represents the global configuration for a set of target repositories
  * linked into other objects under the `GLOBAL` key

* [PkgSpec](PkgSpec.md)
  * represents individual packages

* [PoolSpec](PoolSpec.md)
  * represents a pool

* [TargetSpec](TargetSpec.md)
  * build target

* [DutSpec](DutSpec.md)
  * device under test
