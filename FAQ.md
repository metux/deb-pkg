
Q: What does 'pool' mean here ?

A: Pools are used for organizing sets of packages. Each pool lives entirely on
   it's own, using an own apt repository (in `.aptrepo/<pool>`).

---

Q: How can I define which distros to build for ?

A: Use dck-buildpackage's target configs. The `targets:` section in the config
   yml tells the dck-buildpackage's target names.

---

Q: How can I build for Devuan ? (debootstrap fails to find script 'ascii')

A: Debian's and Ubuntu's version of debootstrap don't know about Devuan releases.
   Just chdir to /usr/share/deboootstrap/scripts/ and create symlinks named by
   the Devuan release (eg. 'ascii') pointing to 'sid'.

---

Q: How can I build for SuSE (SLES) ?

A: You need access to SuSE's repositories, which needs n commercial subscription
   in order to create the base images.

   The directory misc/schroot/sles12 contains some helpful scripts, which
   can create images for use with the 'sles12-x86_64' target.

---

Q: Can I have support for a more recent version of SuSE ?

A: It's a bit tricky for me, as it needs a commercial subscription (which is
   anything but cheap), and SuSE isn't actually comfortable for development.

   Feel free to ask me about commercial consulting ;-)

---

Q: Where can I get dck-buildpackage ? What is that anyways ?

A: It's a little tool for building debian packages in docker containers.
   See: https://github.com/metux/docker-buildpackage

   When using schroot, this tool is not needed, just ignore it.

---

Q: What is CSDB and what is it for ?

A: The CSDB (comprehensive source database) is a little "database" (set of
   yml descriptor files) which holds some canonical metadata for package
   source locations (mainly git repo URL).

   It's devided into several sections, each of them representing a class
   of sources: "upstream" holds the actual upstream projects, "debian"
   is the (usually patched) Debian sources, "oss-qm" is the "opensource
   QM project", which does lots fixes to get a package built and running
   (for different distros).

   In most cases, you'd pull from the OSS-QM project, but you can also add your
   own section by adding it to the global build config's patches->remote-names
   and csdb->sections list, and adding your own customized yaml files in the
   corresponding subdir. Just do it like it's done in the existing ones.

---

Q: How can I build packages that depend on others (that aren't in the distro yet) ?

A: Just add the dependencies to the packages (note: the names you're using in the
   config, not the debian package names). The packages will be built along the
   dependency tree and placed into the pool's repo. This repo is also added to
   the build container's package sources, so apt can automatically install the
   previously built packages from there.

---

Q: How are the sources fetched ?

A: The sources are automatically pulled from the enabled remotes, their URLs
   are picked from CSDB configs. For each package, a separate clone is created
   under the pkg/ subdir - the initially checked out branch is defined in the
   'autobuild-ref' attribute (either globally or per-package)

   You can use it just any normal git repo. Note that you always have to
   commit your changes before building, otherwise the build process won't
   catch them.

---

Q: Why aren't packages rebuilt automatically ?

A: After a package has been successfully built, a flag file is written
   (.stat/ subdir), holding the built git commit ID. If the flag file exists
   and the HEAD commit ID is the same, the package won't be rebuilt.

   Usually that's good, but if you *really* need a rebuild, remove the
   corresponding flag file.

---


Q: How does the package version actually work ?

A: It has two facets: package names with @<version> are in mostly treated like
   normal package names (eg. git repo name), but the build system looks for the
   CSDB descriptor files *without* the @<version> suffix. The version (what's
   after the @) will be available in the ${package.version} variable.

   When refering to packages with version (eg. dependency or in the pool's package
   list) it needs to be written *with* the full name (including @<version>)

---

Q: How can I trigger rebuild of packages that I already had built ?

A: Remove the corresponding state files in `.stat/`

---

Q: Why are there multiple global configs ?

A: In some cases, separate target repos cannot be expressed in the same global
   config, eg. when dependencies or other package attributes are different between
   targets. That's why there may be several distinct global configs.

   It also helps to separate things more clearly.

---

Q: Why does global config have many packages without any attributes ?

A: Most attributes can be derived automatically, from given defaults. But the package
   itself still needs to be defined. That's why those YAML sections are just empty.

---

Q: What is rpm-define for ?

A: rpmbuild supports parameters, which can be used in the spec file. This is eg.
   helpful when a package can be built in different variants or linking against
   separate versions of some other packages (sample usecase: PostgreSQL extensions).

   Passing parameters helps keeping everything in one generic spec file.

---

Q: Where can I find the final apt/zypper repos ?

A: apt repos are stored under the .aptrepo dir, zypper repos under .zyprepo.

   For each pool, a separate repo (by the pool name) is created under the
   .aptrepo / .zyprepo directory. These repos can directly serve for installation.

---

Q: What does 'autobuild-force' mean ?

A: The default behaviour is cloning the git repos only one and nevery overwriting
   any existing ones (neither changing anything). This is good for development,
   but unpleasant for CI.

   When running within a CI, it's desireable to always have a fresh copy, which
   is exactly the defined revision (or the latest one). For this use case, you
   can set 'autobuild-force' to 'true'

   Warning: this mode *destroys* all locally made changes on each build !

---

   