# Repo configurations

Each YAML file defines a build configuration targeting one or more
distributions. They reference git sources from `cf/csdb/` and target
definitions from `cf/targets/`.

## Existing configs

### `devuan/sidplayfp.yml`

Builds sidplayfp with its dependency chain (libresidfp, libsidplayfp) for
Devuan Excalibur. Two pools:

- **sidplayfp-release** — tagged releases (`v1.0.2`, `v3.0.1`, `v3.0.2`)
- **sidplayfp-master** — latest upstream/master (`999-dev` versions)

### `devuan/containers-dev.yml`

Container toolchain packages (runc, containerd, nerdctl, docker-cli) for
multiple Devuan releases (chimaera, daedalus, testing, unstable). Includes
golang toolchain bootstrapping.

### `devuan/go-x11.yml`

The pure-Go X11 protocol library and toolkit (`go-x11proto`), built for
multiple Devuan releases. One source produces three binary packages:
`golang-github-x11libre-go-x11proto-dev` (library sources), `xnamespace`
(X-NAMESPACE client tool) and `tetris64` (demo game). Single pool **go-x11**.
Needs Go >= 1.22 in the build environment.

### `mixed/wine.yml`

Wine 10.20 for both Debian Bookworm and Devuan Daedalus.
