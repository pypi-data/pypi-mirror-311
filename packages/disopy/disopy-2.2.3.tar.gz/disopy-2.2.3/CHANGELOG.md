# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.3] - 2024-11-27
### Changed
- Fix a bug with the new `/stream` endpoint.

## [2.2.2] - 2024-11-24
### Added
- Add a fallback for downloading songs with the `/stream` endpoint.

## [2.2.1] - 2024-11-17
### Changed
- Config files in the example Docker Compose file.
- The `/sync` command now works properly.
- The global Command Tree sync is now done with a system aware when the program has been updated.
- Bump up Knuckles version to fix an [issue](https://github.com/kutu-dev/disopy/issues/16) with [Funkwhale](https://www.funkwhale.audio).

## [2.2.0] - 2024-11-02
### Added
- An option to disable HTTPS and fallback to HTTP.

### Modified
- Bump up the [`knuckles`](https://github.com/kutu-dev/knuckles) library version to `1.1.7`

## [2.1.0] - 2024-11-02
### Added
- Support for adding to the queue albums and playlists.

### Modified
- Embeds with more clear messages, emojis and an error variant.

### Removed
- Modify and save the volume set by the users in the config file (Hard and too niche to implement with multiple guilds in mind).

## [2.0.0] - 2024-11-01

### Added
- A `volume` entry in the config file to set the base volume of all the songs.
- The following commands:
    - `/stop`.
    - `/queue`.
    - `/resume`.
    - `/pause`.
    - `/sync`.
    - `/volume`.
- An acknowledgements section in the `README.md` file.
- CI/CD linting, formatting, publishing and Docker building.
- Publish the package to PyPI.
- Official `Dockerfile` and `compose.yaml` files.
- Official Docker package on the [GitHub Container Registry](ghcr.io).
- Docstrings 100% coverage.
- A [developer section](./CONTRIBUTING.md) in the config file for a better DX.

### Changed
- Bump up the Python version to `3.13.0`.
- The project is now licensed under the [MPL 2.0](https://www.mozilla.org/en-US/MPL/) license instead of the [MIT](https://opensource.org/license/MIT) license.
- The project now uses the [Hatch](https://hatch.pypa.io/latest/) Python project manager.
- Remake and clean the project from the ground up.
- The config file is now in [TOML](https://toml.io/) instead of [JSON](https://www.json.org/).
