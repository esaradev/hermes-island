# Hermes Island

macOS Dynamic Island notch app for Hermes agents. Monitor sessions, fabric memory, and multi-agent workflows from your screen's notch.

## Install

**Download** the latest `.zip` from [Releases](https://github.com/esaradev/hermes-island/releases), unzip, and drag `HermesIsland.app` to Applications.

First launch on an unsigned build: right-click the app > Open, or run:
```bash
xattr -cr /Applications/HermesIsland.app
```

**Build from source** (requires Xcode 16+):
```bash
git clone https://github.com/esaradev/hermes-island.git
cd hermes-island
xcodebuild -scheme HermesIsland -configuration Release build
```

Launch the app. It auto-installs a Hermes plugin at `~/.hermes/plugins/hermes_island/`.

## What it does

A floating notch overlay that expands when your Hermes agent is working:

- **Collapsed** -- agent name, green dot when active
- **Expanded** -- current action, tool being used, session status
- **Full view** -- session transcript, tool results, quick actions

When the [Icarus memory plugin](https://github.com/esaradev/icarus-plugin) is also loaded, the notch shows fabric write/recall events too.

## How it works

```
Hermes Agent
  +-- hermes_island plugin (auto-installed by the app)
        +-- sends events over Unix socket (/tmp/hermes-island.sock)
              +-- HermesIsland.app listens and renders notch UI
```

The plugin hooks into `on_session_start`, `pre_tool_call`, `post_tool_call`, `post_llm_call`, and `on_session_end` to send real-time events.

## Requirements

- macOS 15.0+
- [Hermes](https://github.com/NousResearch/hermes-agent) v0.5.0+

## Support

Free and open source. If you find it useful, [sponsor the project](https://github.com/sponsors/esaradev).

## License

Apache 2.0 (see LICENSE.md)
