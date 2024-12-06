<div align="center" markdown="1">
<h1>Disopy</h1>

[![justforfunnoreally.dev badge](https://img.shields.io/badge/justforfunnoreally-dev-9ff)](https://justforfunnoreally.dev)
![PyPI - Version](https://img.shields.io/pypi/v/disopy)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/disopy)

A Discord bot for listening music from a Subsonic server.
</div>

## Setup
The only external dependencies needed are:
- Python 3.13.0 or higher.
- `ffmpeg`.
- `libopus`.
- `libffi-devel`.

Then just install the bot from [PyPI](https://pypi.org/) with [pipx](https://github.com/pypa/pipx):
```sh
pipx install disopy
```

Or directy with `pip`:
```sh
python3 -m pip install disopy
```

Finally generate a basic config file:
```sh
disopy --generate-config
```

It will be located at `${XDG_CONFIG_DIR}/disopy/config.toml` (in most cases `$HOME/.config/disopy/config.toml`), remember to edit it with your configuration values.

### Docker
There is an official Docker container with name [`ghcr.io/kutu-dev/disopy`](https://github.com/kutu-dev/disopy/pkgs/container/disopy). An [example compose file](./compose.yaml) is also provided.

## Running the bot
The bot needs two environment variables:
### `DISOPY_SUBSONIC_PASSWORD`
The password to be send to the Subsonic REST API. Usually it'll be the same that you use to login in the WebUI of your Subsonic compatible server.

### `DISOPY_DISCORD_TOKEN`
The token to be used when authenticating to the Discord API. To set up a bot on Discord follow this tutorial:
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application.
3. On the application go to `Bot`.
4. Enable `Message Content Intent`.
5. And click on `Reset Token` to get string you should put on the env variable.

#### How to create an invite link
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Enter your bot application.
3. On the application go to `OAuth2`.
4. Copy your `Client ID`.
5. Go to this preconfigured [Discord Permissions Calculator](https://discordapi.com/permissions.html#2184186880).
6. Paste your `Client ID` on the bottom.
7. Copy and share your invite link at the bottom of the web!

And then just start the bot!
```sh
DISOPY_SUBSONIC_PASSWORD=foo DISOPY_DISCORD_TOKEN=bar disopy
```

## Contributing
If you are interested in fixing bugs or adding new features please check the [contributing guide](./CONTRIBUTING.md).

## Acknowledgements
- Created with :heart: by [Jorge "Kutu" Dobón Blanco](https://dobon.dev).
- [JmTexas19](https://github.com/JmTexas19): Creator of [Subrift](https://github.com/JmTexas19/subrift), project forked that served as a base for Disopy.
- [iGieri](https://github.com/iGieri): Fix issue [#1](https://github.com/kutu-dev/disopy/issues/1).
- [outmaneuver](https://github.com/outmaneuver): Fix issue [#3](https://github.com/kutu-dev/disopy/issues/3).
- [An May (YUR0ii)](https://github.com/YUR0ii): Make [HTTPS optional](https://github.com/kutu-dev/disopy/pull/11).
