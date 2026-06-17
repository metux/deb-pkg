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

### `mixed/wine.yml`

Wine 10.20 for both Debian Bookworm and Devuan Daedalus.
