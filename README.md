Debian Chimerea backports
==================================

Preconfigured deb-pkg instance (see down below) to build several
backports for Debian Chimerea.

Little Debian packaging helper
===============================

This is a little tool for making build pipelines for Debian packaging easier.

It automatically clones git repos (which are expected to hold already
debianized trees), builds them along the dependency tree (using my
dck-buildpackage tool) and puts them into installable apt repos.

Configuration is done via yaml. (see packages.yml for an example)

See [FAQ](FAQ.md)

NOTE: documentation is still scarce. Feel free to ask if you have questions.

Contact: Enrico Weigelt, metux IT consult <info@metux.net>
License: AGPL v3
